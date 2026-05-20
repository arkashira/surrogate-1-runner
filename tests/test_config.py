import unittest
import yaml
import json
from surrogate_1.config import ConfigParser

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.valid_yaml = """
        python:
          indent: 4
          line_length: 120
        javascript:
          single_quote: true
          tab_width: 2
        go:
          remove_extra_spaces: true
        """
        self.valid_json = """
        {
          "python": {
            "indent": 4,
            "line_length": 120
          },
          "javascript": {
            "single_quote": true,
            "tab_width": 2
          },
          "go": {
            "remove_extra_spaces": true
          }
        }
        """
        self.invalid_yaml = """
        python:
          indent: 4
          line_length: "120"
        """
        self.invalid_json = """
        {
          "python": {
            "indent": 4,
            "line_length": "120"
          }
        }
        """
        self.missing_key_yaml = """
        python:
          indent: 4
        javascript:
          single_quote: true
        """
        self.missing_key_json = """
        {
          "python": {
            "indent": 4
          },
          "javascript": {
            "single_quote": true
          }
        }
        """
        self.invalid_language_yaml = """
        invalid_language:
          option: value
        """
        self.invalid_language_json = """
        {
          "invalid_language": {
            "option": "value"
          }
        }
        """

    def test_valid_yaml_config(self):
        config = ConfigParser()
        result = config.parse(yaml.safe_load(self.valid_yaml))
        self.assertEqual(result['python']['indent'], 4)
        self.assertEqual(result['javascript']['tab_width'], 2)
        self.assertEqual(result['go']['remove_extra_spaces'], True)

    def test_valid_json_config(self):
        config = ConfigParser()
        result = config.parse(json.loads(self.valid_json))
        self.assertEqual(result['python']['indent'], 4)
        self.assertEqual(result['javascript']['tab_width'], 2)
        self.assertEqual(result['go']['remove_extra_spaces'], True)

    def test_invalid_yaml_config(self):
        config = ConfigParser()
        with self.assertRaises(ValueError):
            config.parse(yaml.safe_load(self.invalid_yaml))

    def test_invalid_json_config(self):
        config = ConfigParser()
        with self.assertRaises(ValueError):
            config.parse(json.loads(self.invalid_json))

    def test_missing_language_key_yaml(self):
        config = ConfigParser()
        result = config.parse(yaml.safe_load(self.missing_key_yaml))
        with self.assertRaises(KeyError):
            result['go']

    def test_missing_language_key_json(self):
        config = ConfigParser()
        result = config.parse(json.loads(self.missing_key_json))
        with self.assertRaises(KeyError):
            result['go']

    def test_invalid_language_yaml(self):
        config = ConfigParser()
        with self.assertRaises(ValueError):
            config.parse(yaml.safe_load(self.invalid_language_yaml))

    def test_invalid_language_json(self):
        config = ConfigParser()
        with self.assertRaises(ValueError):
            config.parse(json.loads(self.invalid_language_json))

if __name__ == '__main__':
    unittest.main()