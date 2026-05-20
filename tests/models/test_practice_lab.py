from src.models.practice_lab import PracticeLab

def test_practice_lab_to_dict():
    lab = PracticeLab(1, 'Lab 1', 'Description for Lab 1', 'Instructions for Lab 1', ['Objective 1', 'Objective 2'], 'Easy', 30)
    lab_dict = lab.to_dict()
    assert lab_dict['id'] == 1
    assert lab_dict['title'] == 'Lab 1'
    assert lab_dict['description'] == 'Description for Lab 1'
    assert lab_dict['instructions'] == 'Instructions for Lab 1'
    assert lab_dict['objectives'] == ['Objective 1', 'Objective 2']
    assert lab_dict['difficulty'] == 'Easy'
    assert lab_dict['duration'] == 30