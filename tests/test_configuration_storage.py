import unittest
import os
import sqlite3
from src.configuration_storage import ConfigurationStorage

class TestConfigurationStorage(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_configurations.db'
        self.storage = ConfigurationStorage(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_init_db(self):
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='configurations'")
            self.assertIsNotNone(cursor.fetchone())

    def test_save_configuration(self):
        config = {
            'data_type': 'metrics',
            'data_volume': 1000,
            'start_timestamp': '2023-01-01T00:00:00',
            'end_timestamp': '2023-01-02T00:00:00'
        }
        config_id = self.storage.save_configuration(config)
        self.assertIsInstance(config_id, int)

    def test_get_configuration(self):
        config = {
            'data_type': 'logs',
            'data_volume': 500,
            'start_timestamp': '2023-01-01T00:00:00',
            'end_timestamp': '2023-01-02T00:00:00'
        }
        config_id = self.storage.save_configuration(config)
        retrieved_config = self.storage.get_configuration(config_id)
        self.assertEqual(retrieved_config['data_type'], 'logs')
        self.assertEqual(retrieved_config['data_volume'], 500)

    def test_get_all_configurations(self):
        config1 = {
            'data_type': 'metrics',
            'data_volume': 1000,
            'start_timestamp': '2023-01-01T00:00:00',
            'end_timestamp': '2023-01-02T00:00:00'
        }
        config2 = {
            'data_type': 'logs',
            'data_volume': 500,
            'start_timestamp': '2023-01-01T00:00:00',
            'end_timestamp': '2023-01-02T00:00:00'
        }
        self.storage.save_configuration(config1)
        self.storage.save_configuration(config2)
        all_configs = self.storage.get_all_configurations()
        self.assertEqual(len(all_configs), 2)

if __name__ == '__main__':
    unittest.main()