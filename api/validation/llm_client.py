import os
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class HypothesisTestResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class LLMHypothesisTester:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.surrogate-1.com/v1"):
        self.api_key = api_key or os.getenv("SURROGATE_1_API_KEY")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> HypothesisTestResult:
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return HypothesisTestResult(
                success=True,
                data=response.json()
            )
        except requests.exceptions.RequestException as e:
            return HypothesisTestResult(
                success=False,
                error=str(e)
            )
    
    def generate_interview_questions(self, hypothesis: str, customer_segment: str = "general") -> HypothesisTestResult:
        payload = {
            "hypothesis": hypothesis,
            "customer_segment": customer_segment,
            "task_type": "interview_questions"
        }
        return self._make_request("/hypothesis/test", payload)
    
    def analyze_competitors(self, hypothesis: str, industry: str = "technology") -> HypothesisTestResult:
        payload = {
            "hypothesis": hypothesis,
            "industry": industry,
            "task_type": "competitor_analysis"
        }
        return self._make_request("/hypothesis/test", payload)
    
    def stress_test_pricing(self, hypothesis: str, pricing_model: str = "subscription") -> HypothesisTestResult:
        payload = {
            "hypothesis": hypothesis,
            "pricing_model": pricing_model,
            "task_type": "pricing_stress_test"
        }
        return self._make_request("/hypothesis/test", payload)
    
    def validate_hypothesis(self, hypothesis: str, validation_type: str) -> HypothesisTestResult:
        payload = {
            "hypothesis": hypothesis,
            "validation_type": validation_type
        }
        return self._make_request("/hypothesis/validate", payload)

# Example usage
if __name__ == "__main__":
    tester = LLMHypothesisTester()
    
    # Test interview questions
    result = tester.generate_interview_questions(
        "Users prefer a simplified dashboard interface"
    )
    if result.success:
        print("Generated questions:", result.data.get("questions", []))
    else:
        print("Error:", result.error)
    
    # Test competitor analysis
    result = tester.analyze_competitors(
        "AI-powered analytics will increase user engagement"
    )
    if result.success:
        print("Competitor analysis:", result.data.get("summary", ""))
    else:
        print("Error:", result.error)
    
    # Test pricing stress test
    result = tester.stress_test_pricing(
        "Freemium model will drive 30% conversion"
    )
    if result.success:
        print("Pricing test results:", result.data.get("scenarios", []))
    else:
        print("Error:", result.error)