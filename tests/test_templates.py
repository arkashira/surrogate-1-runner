import unittest
import yaml
import os

class TestTemplates(unittest.TestCase):
    def test_reddit_template(self):
        with open('templates/library/reddit.yaml', 'r') as file:
            template = yaml.safe_load(file)
        self.assertEqual(template['name'], 'Reddit Data Ingestion')
        self.assertEqual(template['source']['type'], 'reddit')

    def test_github_template(self):
        with open('templates/library/github.yaml', 'r') as file:
            template = yaml.safe_load(file)
        self.assertEqual(template['name'], 'GitHub Data Ingestion')
        self.assertEqual(template['source']['type'], 'github')

    def test_csv_template(self):
        with open('templates/library/csv.yaml', 'r') as file:
            template = yaml.safe_load(file)
        self.assertEqual(template['name'], 'CSV Data Ingestion')
        self.assertEqual(template['source']['type'], 'file')

    def test_twitter_template(self):
        with open('templates/library/twitter.yaml', 'r') as file:
            template = yaml.safe_load(file)
        self.assertEqual(template['name'], 'Twitter Data Ingestion')
        self.assertEqual(template['source']['type'], 'twitter')

    def test_json_template(self):
        with open('templates/library/json.yaml', 'r') as file:
            template = yaml.safe_load(file)
        self.assertEqual(template['name'], 'JSON Data Ingestion')
        self.assertEqual(template['source']['type'], 'file')

if __name__ == '__main__':
    unittest.main()