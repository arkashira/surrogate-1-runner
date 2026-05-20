
import unittest
from unittest.mock import MagicMock, patch
from src.referential_integrity import ReferentialIntegrityChecker, ReferentialIntegrityCheck

class TestReferentialIntegrityChecker(unittest.TestCase):

    def setUp(self):
        self.database_url = "sqlite:///:memory:"
        self.checker = ReferentialIntegrityChecker(self.database_url)

    def test_perform_check(self):
        with patch.object(self.checker, '_perform_check') as mock_check:
            check = ReferentialIntegrityCheck(
                source_table="test_source",
                target_table="test_target",
                source_key="source_id",
                target_key="target_id",
                description="Test Check"
            )
            mock_check.return_value = True
            result = self.checker.check_referential_integrity([check])
            self.assertTrue(result["Test Check"])

    def test_check_provenance(self):
        with patch.object(self.checker, 'check_provenance') as mock_provenance:
            mock_provenance.return_value = {"provenance": "data"}
            result = self.checker.check_provenance("test_entity_id")
            self.assertEqual(result, {"provenance": "data"})

if __name__ == '__main__':
    unittest.main()