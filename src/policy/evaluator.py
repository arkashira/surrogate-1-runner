import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PolicyRule:
    id: str
    condition: Dict[str, Any]
    action: str
    priority: int = 0

@dataclass
class Policy:
    id: str
    version: str
    rules: List[PolicyRule]
    metadata: Dict[str, Any]

@dataclass
class EvaluationResult:
    decision: str
    trace: List[Dict[str, Any]]

class PolicyEvaluator:
    def __init__(self):
        self.policies: Dict[str, List[Policy]] = {}
    
    def load_policy(self, policy_json: str) -> Policy:
        """Load a policy from JSON string"""
        data = json.loads(policy_json)
        
        # Validate required fields
        required_fields = ['id', 'version', 'rules']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert rules to PolicyRule objects
        rules = []
        for rule_data in data['rules']:
            rule = PolicyRule(
                id=rule_data['id'],
                condition=rule_data['condition'],
                action=rule_data['action'],
                priority=rule_data.get('priority', 0)
            )
            rules.append(rule)
        
        return Policy(
            id=data['id'],
            version=data['version'],
            rules=rules,
            metadata=data.get('metadata', {})
        )
    
    def evaluate(self, policy_id: str, input_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate input data against a policy and return decision with trace"""
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        
        # Get latest version of the policy
        policy = max(self.policies[policy_id], key=lambda p: p.version)
        
        matched_rules = []
        
        # Sort rules by priority (higher first)
        sorted_rules = sorted(policy.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if self._matches_condition(rule.condition, input_data):
                matched_rules.append({
                    'rule_id': rule.id,
                    'condition': rule.condition,
                    'action': rule.action,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Return immediately on first match (assuming first match wins)
                return EvaluationResult(
                    decision=rule.action,
                    trace=matched_rules
                )
        
        # No rules matched
        return EvaluationResult(
            decision="default",
            trace=matched_rules
        )
    
    def _matches_condition(self, condition: Dict[str, Any], input_data: Dict[str, Any]) -> bool:
        """Check if input data matches the condition"""
        for key, expected_value in condition.items():
            if key not in input_data:
                return False
            
            actual_value = input_data[key]
            
            # Handle different types of conditions
            if isinstance(expected_value, dict):
                # Support for operators like $eq, $gt, etc.
                if '$eq' in expected_value:
                    if actual_value != expected_value['$eq']:
                        return False
                elif '$gt' in expected_value:
                    if actual_value <= expected_value['$gt']:
                        return False
                elif '$lt' in expected_value:
                    if actual_value >= expected_value['$lt']:
                        return False
                elif '$in' in expected_value:
                    if actual_value not in expected_value['$in']:
                        return False
                else:
                    # Direct value comparison for nested dicts
                    if actual_value != expected_value:
                        return False
            else:
                # Direct value comparison
                if actual_value != expected_value:
                    return False
        
        return True
    
    def add_policy(self, policy: Policy):
        """Add a policy to the evaluator"""
        if policy.id not in self.policies:
            self.policies[policy.id] = []
        self.policies[policy.id].append(policy)
    
    def get_policy_history(self, policy_id: str) -> List[Policy]:
        """Get version history for a policy"""
        if policy_id not in self.policies:
            return []
        return sorted(self.policies[policy_id], key=lambda p: p.version)