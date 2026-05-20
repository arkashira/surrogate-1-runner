import unittest
from lab_progress_service import LabProgressService

class TestLabProgressService(unittest.TestCase):
    def test_add_lab_path(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        self.assertIn("lab_path_1", service.lab_paths)
        self.assertIn("lab_path_1", service.progress)

    def test_update_progress(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        service.update_progress("lab_path_1", "challenge_1", True)
        self.assertTrue(service.get_progress("lab_path_1")["challenge_1"])

    def test_get_progress(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        self.assertEqual(service.get_progress("lab_path_1"), {"challenge_1": False, "challenge_2": False})

    def test_get_completion_badge(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        service.update_progress("lab_path_1", "challenge_1", True)
        self.assertEqual(service.get_completion_badge("lab_path_1"), "1/2")

    def test_to_json(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        service.update_progress("lab_path_1", "challenge_1", True)
        json_str = service.to_json()
        self.assertIn("lab_path_1", json_str)

    def test_from_json(self):
        service = LabProgressService()
        service.add_lab_path("lab_path_1", ["challenge_1", "challenge_2"])
        service.update_progress("lab_path_1", "challenge_1", True)
        json_str = service.to_json()
        new_service = LabProgressService.from_json(json_str)
        self.assertEqual(new_service.get_progress("lab_path_1"), {"challenge_1": True, "challenge_2": False})

if __name__ == "__main__":
    unittest.main()