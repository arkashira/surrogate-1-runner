import unittest
from customization_storage import CustomizationStorage

class TestCustomizationStorage(unittest.TestCase):
    def setUp(self):
        self.storage = CustomizationStorage(storage_path='test_customization_storage.json')

    def tearDown(self):
        if os.path.exists('test_customization_storage.json'):
            os.remove('test_customization_storage.json')

    def test_set_and_get_prompt(self):
        self.storage.set_prompt('test_key', 'test_value')
        self.assertEqual(self.storage.get_prompt('test_key'), 'test_value')

    def test_set_and_get_command(self):
        self.storage.set_command('test_key', 'test_value')
        self.assertEqual(self.storage.get_command('test_key'), 'test_value')

    def test_delete_prompt(self):
        self.storage.set_prompt('test_key', 'test_value')
        self.storage.delete_prompt('test_key')
        self.assertIsNone(self.storage.get_prompt('test_key'))

    def test_delete_command(self):
        self.storage.set_command('test_key', 'test_value')
        self.storage.delete_command('test_key')
        self.assertIsNone(self.storage.get_command('test_key'))

if __name__ == '__main__':
    unittest.main()