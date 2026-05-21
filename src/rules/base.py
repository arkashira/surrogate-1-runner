from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Rule(ABC):
    """
    Abstract base class for all custom detection rules.
    
    Each rule must implement the 'evaluate' method which takes a context 
    and returns a boolean indicating whether the rule condition is met.
    Additionally, each rule should provide its name, severity, and description.
    """

    def __init__(self, name: str, severity: str = "medium", description: str = ""):
        """
        Initialize a rule with a name, severity level, and description.
        
        :param name: Unique identifier for the rule
        :param severity: Severity level (low, medium, high, critical)
        :param description: Description of the rule
        """
        self._name = name
        self._severity = severity
        self._description = description

    @property
    def name(self) -> str:
        """Name of the rule."""
        return self._name

    @property
    def severity(self) -> str:
        """Severity level of the rule (e.g., 'low', 'medium', 'high', 'critical')."""
        return self._severity

    @property
    def description(self) -> str:
        """Description of the rule."""
        return self._description

    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> bool:
        """
        Evaluate the rule against the given data.
        
        :param data: The data to evaluate the rule against.
        :return: True if the rule condition is met, False otherwise.
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this rule.
        
        :return: Dictionary containing rule metadata
        """
        return {
            "name": self.name,
            "severity": self.severity,
            "description": self.description,
            "type": self.__class__.__name__
        }

# src/rules/test_base.py
import unittest
from src.rules.base import Rule

class TestRule(unittest.TestCase):
    def test_rule_abstract_methods(self):
        """Test that Rule is an abstract class with required methods."""
        self.assertTrue(hasattr(Rule, 'name'))
        self.assertTrue(hasattr(Rule, 'severity'))
        self.assertTrue(hasattr(Rule, 'description'))
        self.assertTrue(hasattr(Rule, 'evaluate'))

        with self.assertRaises(TypeError):
            Rule("TestRule")

    def test_rule_metadata(self):
        """Test that Rule correctly returns metadata."""
        class ConcreteRule(Rule):
            def evaluate(self, data: Dict[str, Any]) -> bool:
                return True
        
        rule = ConcreteRule(name="TestRule", severity="high", description="A test rule")
        metadata = rule.get_metadata()
        self.assertEqual(metadata["name"], "TestRule")
        self.assertEqual(metadata["severity"], "high")
        self.assertEqual(metadata["description"], "A test rule")
        self.assertEqual(metadata["type"], "ConcreteRule")

if __name__ == '__main__':
    unittest.main()