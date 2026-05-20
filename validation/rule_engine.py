import yaml
import re
from pathlib import Path

class RuleEngine:
    def __init__(self, rules_file_path='/compliance/rules.yaml'):
        self.rules_file_path = rules_file_path
        self.rules = self.load_rules()

    def load_rules(self):
        with open(self.rules_file_path, 'r') as file:
            return yaml.safe_load(file)

    def validate(self, data):
        for rule in self.rules:
            if 'pattern' in rule:
                pattern = rule['pattern']
                if not re.match(pattern, data):
                    return False
        return True

def main():
    rule_engine = RuleEngine()
    test_data = "example_data"
    if rule_engine.validate(test_data):
        print("Data is compliant.")
    else:
        print("Data is not compliant.")

if __name__ == "__main__":
    main()