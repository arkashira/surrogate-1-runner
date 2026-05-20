import unittest
import os
import tempfile
from src.sop_creator import SOPCreator

class TestSOPCreator(unittest.TestCase):
    def setUp(self):
        self.templates_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        self.sop_creator = SOPCreator(self.templates_dir, self.output_dir)

        # Create a test template
        with open(os.path.join(self.templates_dir, 'test_template.md'), 'w') as f:
            f.write("This is a test template with variable {{variable1}} and {{variable2}}.")

    def test_list_templates(self):
        templates = self.sop_creator.list_templates()
        self.assertIn('test_template.md', templates)

    def test_create_sop(self):
        variables = {'variable1': 'value1', 'variable2': 'value2'}
        output_path = self.sop_creator.create_sop('test_template.md', variables)
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, 'r') as f:
            content = f.read()
            self.assertIn('value1', content)
            self.assertIn('value2', content)

    def tearDown(self):
        for root, dirs, files in os.walk(self.templates_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.templates_dir)

        for root, dirs, files in os.walk(self.output_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()