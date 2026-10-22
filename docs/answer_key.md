# Answer Key: Known Defects

> **Do not open this until you have run the tests and written your own bug reports.**
> Then compare: did you find all three, and is your root cause the same?

The application ships with **3 seeded defects**. They make **6 automated tests fail** (plus 1 UI test).

| Bug | Where | What is wrong | Failing tests | Severity |
|---|---|---|---|---|
| 1 | `app/grading.py`, `grade()` | `if avg > 80` should be `if avg >= 80`. An average of exactly 80 gets **A** instead of **A+**. | `test_grade_boundaries[80-A+]`, `test_TC14_result_at_grade_boundary` | High |
| 2 | `app/grading.py`, `validate_mark()` | Only the upper limit is checked (`mark > 100`). Negative marks such as -5 are **accepted and saved**. | `test_invalid_marks_rejected[-1]`, `[-50]`, `test_TC10_negative_marks_rejected`, `test_UI06_negative_marks_show_error` | High |
| 3 | `app/main.py`, `add_student()` | No check for an existing roll. Two students can have **the same roll**, and the result page shows only the first one. | `test_TC12_duplicate_roll_rejected` | High |

## Fixes

**Bug 1**
```python
if avg >= 80:
    return "A+", 4.00
```

**Bug 2**
```python
if mark < 0 or mark > 100:
    raise ValueError("Marks must be between 0 and 100")
```

**Bug 3** (in `add_student()`, before the INSERT)
```python
if roll and get_db().execute("SELECT 1 FROM students WHERE roll = ?", (roll,)).fetchone():
    errors.append("Roll already exists")
```

After the fixes, run `pytest` again: all tests should pass. That is **regression testing**: making sure the fix works and nothing else broke.
