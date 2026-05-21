import unittest
from src.models import ModelRegistry, ApprovedModel

class TestModelRegistry(unittest.TestCase):
    def test_add_approved_model(self):
        registry = ModelRegistry()
        model = ApprovedModel('Claude', 'Large Language Model')
        registry.add_approved_model(model)
        self.assertEqual(len(registry.get_approved_models()), 1)

    def test_get_approved_models(self):
        registry = ModelRegistry()
        model1 = ApprovedModel('Claude', 'Large Language Model')
        model2 = ApprovedModel('Bert', 'Pre-trained Language Model')
        registry.add_approved_model(model1)
        registry.add_approved_model(model2)
        self.assertEqual(len(registry.get_approved_models()), 2)

if __name__ == '__main__':
    unittest.main()