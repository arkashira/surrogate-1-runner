import pandas as pd
import hashlib
from typing import List, Dict

class Anonymizer:
    def __init__(self, salt: str):
        self.salt = salt

    def anonymize(self, data: Dict[str, str]) -> Dict[str, str]:
        anonymized_data = {}
        for key, value in data.items():
            anonymized_value = self._hash_value(value)
            anonymized_data[key] = anonymized_value
        return anonymized_data

    def _hash_value(self, value: str) -> str:
        hasher = hashlib.sha256()
        hasher.update((value + self.salt).encode('utf-8'))
        return hasher.hexdigest()

def anonymize_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Anonymize data by removing sensitive information and replacing sensitive values.
    """
    # Remove personally identifiable information (PII)
    data.drop(['name', 'email', 'phone'], axis=1, inplace=True)
    
    # Remove sensitive columns
    data.drop(['credit_card_number', 'social_security_number'], axis=1, inplace=True)
    
    # Replace sensitive values with anonymized values
    data['credit_card_number'] = data['credit_card_number'].apply(lambda x: 'XXXX-XXXX-XXXX-XXXX')
    data['social_security_number'] = data['social_security_number'].apply(lambda x: 'XXX-XX-XXXX')
    
    # Anonymize data using Anonymizer class
    anonymizer = Anonymizer(salt="your_salt")
    anonymized_data = data.applymap(lambda x: anonymizer._hash_value(str(x)) if isinstance(x, str) else x)
    
    return anonymized_data

def aggregate_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data by industry and stack size.
    """
    # Group data by industry and stack size
    aggregated_data = data.groupby(['industry', 'stack_size']).size().reset_index(name='count')
    
    return aggregated_data

def get_top_optimization_patterns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Get top 5 optimization patterns from similar organizations.
    """
    # Calculate top 5 optimization patterns
    top_patterns = data.nlargest(5, 'count')
    
    return top_patterns