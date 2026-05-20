from src.services.practice_lab_service import PracticeLabService

def test_get_practice_labs():
    practice_labs = PracticeLabService.get_practice_labs()
    assert len(practice_labs) >= 3

def test_get_practice_labs_by_objective():
    practice_labs = PracticeLabService.get_practice_labs(objective='Objective 1')
    assert len(practice_labs) == 2

def test_get_practice_labs_by_difficulty():
    practice_labs = PracticeLabService.get_practice_labs(difficulty='Easy')
    assert len(practice_labs) == 1

def test_get_practice_lab_by_id():
    practice_lab = PracticeLabService.get_practice_lab_by_id(1)
    assert practice_lab.id == 1

def test_get_practice_lab_by_id_not_found():
    practice_lab = PracticeLabService.get_practice_lab_by_id(999)
    assert practice_lab is None