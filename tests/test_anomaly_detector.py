import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    
    def setUp(self):
        self.detector = AnomalyDetector()
        
    def test_detect_anomalies_empty_data(self):
        """Test anomaly detection with empty data"""
        df = pd.DataFrame(columns=['timestamp', 'provider', 'service', 'amount_usd'])
        result = self.detector.detect_anomalies(df)
        self.assertEqual(len(result), 0)
        
    def test_detect_anomalies_single_service_no_anomalies(self):
        """Test detection with normal data that should not trigger anomalies"""
        # Create data with consistent daily amounts
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(10)]
        amounts = [100.0] * 10  # Consistent amounts
        
        df = pd.DataFrame({
            'timestamp': dates,
            'provider': ['aws'] * 10,
            'service': ['ec2'] * 10,
            'amount_usd': amounts
        })
        
        result = self.detector.detect_anomalies(df)
        self.assertEqual(len(result), 0)
        
    def test_detect_anomalies_with_anomalies(self):
        """Test detection with clear anomalies"""
        # Create data with one outlier
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(10)]
        amounts = [100.0] * 9 + [1000.0]  # One large spike
        
        df = pd.DataFrame({
            'timestamp': dates,
            'provider': ['aws'] * 10,
            'service': ['ec2'] * 10,
            'amount_usd': amounts
        })
        
        result = self.detector.detect_anomalies(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['service'], 'ec2')
        self.assertEqual(result[0]['provider'], 'aws')
        self.assertGreater(result[0]['deviation_pct'], 100)
        
    def test_detect_anomalies_multiple_services(self):
        """Test detection with multiple services"""
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(5)]
        amounts = [100.0] * 5
        
        df = pd.DataFrame({
            'timestamp': dates * 2,
            'provider': ['aws'] * 10,
            'service': ['ec2'] * 5 + ['s3'] * 5,
            'amount_usd': amounts + [1000.0] + amounts[1:]  # S3 has an anomaly
        })
        
        result = self.detector.detect_anomalies(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['service'], 's3')
        
    def test_calculate_z_scores(self):
        """Test z-score calculation"""
        data = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 1000.0]
        z_scores = self.detector._calculate_z_scores(data)
        self.assertEqual(len(z_scores), len(data))
        # The last value should have a high z-score
        self.assertGreater(abs(z_scores[-1]), 3.0)
        
    def test_3sigma_rule(self):
        """Test 3-sigma rule implementation"""
        data = [100.0] * 10 + [1000.0]  # One outlier
        z_scores = self.detector._calculate_z_scores(data)
        anomalies = self.detector._apply_3sigma_rule(z_scores)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0], 10)  # Index of the outlier
        
    def test_group_by_service_and_calculate_stats(self):
        """Test grouping and statistics calculation"""
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(5)]
        df = pd.DataFrame({
            'timestamp': dates,
            'provider': ['aws'] * 5,
            'service': ['ec2'] * 5,
            'amount_usd': [100.0, 100.0, 100.0, 100.0, 1000.0]
        })
        
        grouped_stats = self.detector._group_by_service_and_calculate_stats(df)
        self.assertIn('ec2', grouped_stats)
        stats = grouped_stats['ec2']
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        
    def test_no_anomalies_below_threshold(self):
        """Test that small deviations don't trigger anomalies"""
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(10)]
        amounts = [100.0] * 9 + [110.0]  # Small deviation
        
        df = pd.DataFrame({
            'timestamp': dates,
            'provider': ['aws'] * 10,
            'service': ['ec2'] * 10,
            'amount_usd': amounts
        })
        
        result = self.detector.detect_anomalies(df)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()