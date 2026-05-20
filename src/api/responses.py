from .compliance.rule_engine import ComplianceRuleEngine

class ApiResponse:
    def __init__(self, data):
        self.data = data
        self.compliance_engine = ComplianceRuleEngine()

    def add_compliance_status(self):
        compliance_results = self.compliance_engine.check_compliance(self.data)
        self.data['compliance_status'] = compliance_results
        return self.data

# Example usage
if __name__ == "__main__":
    api_response = ApiResponse({'id': 'resource1', 'type': 'aws-s3-bucket'})
    response_with_compliance = api_response.add_compliance_status()
    print(response_with_compliance)