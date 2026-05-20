from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
import time
import asyncio

router = APIRouter()

class TestCoverage(BaseModel):
    test_id: str
    coverage_impact: str  # high/medium/low

class FilteredTestsResponse(BaseModel):
    tests: List[TestCoverage]

async def fetch_test_coverage() -> List[TestCoverage]:
    # Simulate fetching test coverage data from a database or service
    await asyncio.sleep(0.1)  # Simulate IO-bound operation
    return [
        TestCoverage(test_id="test1", coverage_impact="high"),
        TestCoverage(test_id="test2", coverage_impact="medium"),
        TestCoverage(test_id="test3", coverage_impact="low"),
    ]

@router.get("/api/v1/test-filter", response_model=FilteredTestsResponse)
async def filter_tests_by_coverage():
    start_time = time.time()
    
    tests = await fetch_test_coverage()
    
    # Sort tests by coverage impact
    sorted_tests = sorted(tests, key=lambda x: x.coverage_impact, reverse=True)
    
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        raise HTTPException(status_code=504, detail="Request took longer than 500ms")
    
    return {"tests": sorted_tests}

# For CI/CD integration via API webhook
@router.post("/api/v1/test-filter/webhook")
async def handle_webhook(data: dict):
    # Process incoming webhook data and trigger test filtering
    filtered_tests = await filter_tests_by_coverage()
    return {"status": "success", "filtered_tests": filtered_tests}