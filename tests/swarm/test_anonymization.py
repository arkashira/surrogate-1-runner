import unittest
import pandas as pd
from src.swarm.anonymization import anonymize_data, aggregate_data, get_top_optimization_patterns

class TestAnonymization(unittest.TestCase):
    def test_anonymize_data(self):
        # Create test data
        data = pd.DataFrame({
            'name': ['John', 'Jane', 'Bob'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
            'phone': ['123-456-7890', '987-654-3210', '555-555-5555'],
            'credit_card_number': ['1234-5678-9012-3456', '9876-5432-1098-7654', '1111-2222-3333-4444'],
            'social_security_number': ['123-45-6789', '987-65-4321', '111-22-3333']
        })
        
        # Anonymize data
        anonymized_data = anonymize_data(data)
        
        # Check if PII is removed
        self.assertFalse('name' in anonymized_data.columns)
        self.assertFalse('email' in anonymized_data.columns)
        self.assertFalse('phone' in anonymized_data.columns)
        
        # Check if sensitive values are anonymized
        self.assertTrue(anonymized_data['credit_card_number'].apply(lambda x: x == 'XXXX-XXXX-XXXX-XXXX').all())
        self.assertTrue(anonymized_data['social_security_number'].apply(lambda x: x == 'XXX-XX-XXXX').all())
    
    def test_aggregate_data(self):
        # Create test data
        data = pd.DataFrame({
            'industry': ['Finance', 'Finance', 'Retail', 'Retail'],
            'stack_size': ['Small', 'Medium', 'Small', 'Large'],
            'count': [10, 20, 30, 40]
        })
        
        # Aggregate data
        aggregated_data = aggregate_data(data)
        
        # Check if data is aggregated correctly
        self.assertTrue(aggregated_data['industry'].nunique() == 2)
        self.assertTrue(aggregated_data['stack_size'].nunique() == 2)
    
    def test_get_top_optimization_patterns(self):
        # Create test data
        data = pd.DataFrame({
            'industry': ['Finance', 'Finance', 'Retail', 'Retail'],
            'stack_size': ['Small', 'Medium', 'Small', 'Large'],
            'count': [10, 20, 30, 40]
        })
        
        # Get top 5 optimization patterns
        top_patterns = get_top_optimization_patterns(data)
        
        # Check if top 5 patterns are returned
        self.assertTrue(top_patterns.shape[0] == 5)

if __name__ == '__main__':
    unittest.main()