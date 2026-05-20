import pytest

from src.severity import classify_severity, is_high_severity, IMPACT_MATRIX


@pytest.mark.parametrize(
    "impact,expected",
    [
        (0, "Low"),
        (1, "Low"),
        (3, "Low"),
        (4, "Medium"),
        (5, "Medium"),
        (7, "Medium"),
        (8, "High"),
        (9, "High"),
        (10, "High"),
    ],
)
def test_classify_severity_bounds(impact, expected):
    assert classify_severity(impact) == expected


def test_classify_severity_invalid_negative():
    with pytest.raises(ValueError, match="non‑negative"):
        classify_severity(-1)


def test_classify_severity_out_of_range():
    # 11 is outside the defined ranges (0-10)
    with pytest.raises(ValueError, match="outside the defined severity ranges"):
        classify_severity(11)


@pytest.mark.parametrize(
    "impact,expected",
    [
        (0, False),
        (4, False),
        (8, True),
        (10, True),
    ],
)
def test_is_high_severity(impact, expected):
    assert is_high_severity(impact) is expected