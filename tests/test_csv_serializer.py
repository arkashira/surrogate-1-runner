import unittest
from src.report.csv_serializer import serialize_to_csv

class TestCSVSerializer(unittest.TestCase):
    def test_serialize_to_csv(self):
        data = [
            {
                "month": "2023-01",
                "total_spend_usd": 1000,
                "spend_change_pct": 5.0,
                "service": "AWS",
                "service_spend_usd": 800,
                "recommendation": "Optimize EC2 instances",
                "recommendation_savings_usd": 200
            }
        ]
        
        expected_csv = """month,total_spend_usd,spend_change_pct,service,service_spend_usd,recommendation,recommendation_savings_usd
2023-01,1000,5.0,AWS,800,Optimize EC2 instances,200
"""
        
        csv_data = serialize_to_csv(data)
        self.assertEqual(csv_data, expected_csv)

if __name__ == '__main__':
    unittest.main()