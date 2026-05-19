"""
Celery task to perform nightly matching between providers and investors.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any

import boto3
from celery import shared_task

# Mock models (replace with actual ORM models when available)
class Provider:
    id: int
    stage: str
    ticket_size: float
    focus_areas: List[str]
    location: str

    @staticmethod
    def all() -> List["Provider"]:
        # TODO: Replace with real DB query
        return []

class Investor:
    id: int
    stage: str
    max_ticket_size: float
    focus_areas: List[str]
    location: str

    @staticmethod
    def all() -> List["Investor"]:
        # TODO: Replace with real DB query
        return []

class Match:
    provider_id: int
    investor_id: int
    score: int
    created_at: datetime

    @staticmethod
    def bulk_create(matches: List["Match"]) -> None:
        # TODO: Implement actual bulk insert logic
        pass

# Initialize CloudWatch client
cloudwatch = boto3.client("logs", region_name="us-east-1")
LOG_GROUP = "/surrogate-1/matching"
LOG_STREAM = f"matching-{datetime.utcnow().strftime('%Y-%m-%d')}"

def log_to_cloudwatch(message: str):
    """Log messages to AWS CloudWatch."""
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    try:
        cloudwatch.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            logEvents=[{"timestamp": timestamp, "message": message}],
        )
    except Exception as e:
        print(f"[ERROR] Failed to send log to CloudWatch: {e}")

# Scoring function
def score_pair(provider: Provider, investor: Investor) -> int:
    """
    Compute a normalized score (0–100) based on:
    - Stage match (20 pts)
    - Ticket size compatibility (20 pts)
    - Focus area overlap (30 pts)
    - Geographic fit (30 pts)
    """
    score = 0

    # Stage match
    if provider.stage == investor.stage:
        score += 20

    # Ticket size compatibility
    if investor.max_ticket_size >= provider.ticket_size:
        score += 20

    # Focus area overlap
    overlap = set(provider.focus_areas).intersection(set(investor.focus_areas))
    if provider.focus_areas:
        focus_score = (len(overlap) / len(provider.focus_areas)) * 30
        score += round(focus_score)

    # Geographic fit
    if provider.location == investor.location:
        score += 30

    return min(score, 100)

@shared_task(name="backend.tasks.matching.run_matching_job")
def run_matching_job() -> Dict[str, Any]:
    """
    Run nightly matching between providers and investors.
    Returns statistics about processed matches.
    """
    logger = logging.getLogger("matching_job")
    logger.info("Starting nightly matching job.")

    providers = Provider.all()
    investors = Investor.all()

    matches_to_save: List[Match] = []
    total_score = 0
    match_count = 0

    for provider in providers:
        for investor in investors:
            score = score_pair(provider, investor)
            if score >= 70:
                match = Match()
                match.provider_id = provider.id
                match.investor_id = investor.id
                match.score = score
                match.created_at = datetime.utcnow()
                matches_to_save.append(match)
                total_score += score
                match_count += 1

    if matches_to_save:
        Match.bulk_create(matches_to_save)

    avg_score = total_score / match_count if match_count else 0
    result = {
        "matches": match_count,
        "avg_score": round(avg_score, 2),
        "timestamp": datetime.utcnow().isoformat(),
    }

    logger.info(f"Matching job completed: {match_count} matches, avg score {avg_score:.2f}")
    log_to_cloudwatch(f"Nightly matching job: {match_count} matches, avg score {avg_score:.2f}")

    return result