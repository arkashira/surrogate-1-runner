"""
A minimal, self‑contained CLI that prints the battery health score,
a timestamp, and a recommendation.  It exits with 0 if the score is
≥ 50, otherwise 1.
"""

import sys
from datetime import datetime
from .health import get_battery_health_score

def main(argv=None) -> int:
    score = get_battery_health_score()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recommendation = (
        "Replace the battery soon."
        if score < 50
        else "Battery is in good condition."
    )
    print(
        f"Battery health score: {score} "
        f"({'OK' if score >= 50 else 'CRITICAL'})\n"
        f"Last updated: {timestamp}\n"
        f"Recommendation: {recommendation}"
    )
    return 0 if score >= 50 else 1

if __name__ == "__main__":
    sys.exit(main())