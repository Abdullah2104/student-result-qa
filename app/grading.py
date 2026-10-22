"""Grading rules (Bangladesh UGC uniform grading scale).

| Average marks | Letter grade | Grade point |
|---------------|--------------|-------------|
| 80 - 100      | A+           | 4.00        |
| 75 - 79       | A            | 3.75        |
| 70 - 74       | A-           | 3.50        |
| 65 - 69       | B+           | 3.25        |
| 60 - 64       | B            | 3.00        |
| 55 - 59       | B-           | 2.75        |
| 50 - 54       | C+           | 2.50        |
| 45 - 49       | C            | 2.25        |
| 40 - 44       | D            | 2.00        |
| 0  - 39       | F            | 0.00        |

These rules are the specification. The tests check the code against this table.
"""

SUBJECTS = ["Bangla", "English", "Mathematics"]


def average(marks):
    """Average of a list of subject marks, rounded to 2 decimals."""
    if not marks:
        raise ValueError("marks list is empty")
    return round(sum(marks) / len(marks), 2)


def grade(avg):
    """Return (letter_grade, grade_point) for an average mark from 0 to 100."""
    if avg < 0 or avg > 100:
        raise ValueError("average must be between 0 and 100")

    if avg >= 80:
        return "A+", 4.00
    if avg >= 75:
        return "A", 3.75
    if avg >= 70:
        return "A-", 3.50
    if avg >= 65:
        return "B+", 3.25
    if avg >= 60:
        return "B", 3.00
    if avg >= 55:
        return "B-", 2.75
    if avg >= 50:
        return "C+", 2.50
    if avg >= 45:
        return "C", 2.25
    if avg >= 40:
        return "D", 2.00
    return "F", 0.00


def validate_mark(value):
    """Convert a form value to an int mark. Raise ValueError if it is not a valid mark (0-100)."""
    try:
        mark = int(value)
    except (TypeError, ValueError):
        raise ValueError("Marks must be a whole number")
    if mark < 0 or mark > 100:
        raise ValueError("Marks must be between 0 and 100")
    return mark
