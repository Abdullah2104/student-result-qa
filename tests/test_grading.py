"""Unit tests for app/grading.py.

Techniques used:
- Boundary Value Analysis (BVA): test exactly at, just below and just above every grade boundary.
- Equivalence Partitioning (EP): one value from inside each grade band.
- Negative testing: invalid inputs must be rejected.
"""
import pytest

from app.grading import average, grade, validate_mark

# ---------- Boundary Value Analysis on grade() ----------
# Each pair is (average, expected letter grade) taken from the grading table in the spec.
BOUNDARIES = [
    (100, "A+"), (80, "A+"), (79.99, "A"),
    (75, "A"), (74.99, "A-"),
    (70, "A-"), (69.99, "B+"),
    (65, "B+"), (64.99, "B"),
    (60, "B"), (59.99, "B-"),
    (55, "B-"), (54.99, "C+"),
    (50, "C+"), (49.99, "C"),
    (45, "C"), (44.99, "D"),
    (40, "D"), (39.99, "F"),
    (0, "F"),
]


@pytest.mark.parametrize("avg, expected", BOUNDARIES)
def test_grade_boundaries(avg, expected):
    letter, _ = grade(avg)
    assert letter == expected, f"average {avg} should be {expected}, got {letter}"


# ---------- Equivalence Partitioning: one value inside each band ----------
@pytest.mark.parametrize("avg, expected_letter, expected_point", [
    (90, "A+", 4.00), (77, "A", 3.75), (72, "A-", 3.50), (67, "B+", 3.25), (62, "B", 3.00),
    (57, "B-", 2.75), (52, "C+", 2.50), (47, "C", 2.25), (42, "D", 2.00), (20, "F", 0.00),
])
def test_grade_points(avg, expected_letter, expected_point):
    assert grade(avg) == (expected_letter, expected_point)


@pytest.mark.parametrize("bad_avg", [-1, -0.01, 100.01, 150])
def test_grade_rejects_out_of_range(bad_avg):
    with pytest.raises(ValueError):
        grade(bad_avg)


# ---------- average() ----------
def test_average_rounds_to_two_decimals():
    assert average([80, 75, 70]) == 75.0
    assert average([85, 78, 90]) == 84.33


def test_average_empty_list():
    with pytest.raises(ValueError):
        average([])


# ---------- validate_mark() ----------
@pytest.mark.parametrize("value, expected", [("0", 0), ("1", 1), ("50", 50), ("99", 99), ("100", 100)])
def test_valid_marks(value, expected):
    assert validate_mark(value) == expected


@pytest.mark.parametrize("value", ["-1", "-50", "101", "abc", "", None, "45.5"])
def test_invalid_marks_rejected(value):
    with pytest.raises(ValueError):
        validate_mark(value)
