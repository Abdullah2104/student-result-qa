# Test Plan: Student Result Management System

| Item | Detail |
|---|---|
| Application | Student Result Management System (Flask web app) |
| Version under test | 1.0 |
| Prepared by | Md. Abdullah Mandal |
| Date | _fill in_ |

## 1. Objective
Verify that the system lets an admin log in, add students with marks, and view each student’s result with the correct average, letter grade and GPA, according to the grading table in `app/grading.py`.

## 2. Scope

**In scope**
- Login and logout, and access control for protected pages
- Add student form: required fields and marks validation
- Result calculation: average, letter grade, GPA (Bangladesh UGC scale)
- Student list

**Out of scope**
- Performance and load testing
- Security testing beyond basic access control
- Editing or deleting students (not implemented)

## 3. Test approach

| Level | What | How | Where |
|---|---|---|---|
| Unit | Grading and validation functions | pytest, boundary value analysis, equivalence partitioning | `tests/test_grading.py` |
| Functional / integration | Each feature through HTTP requests | pytest + Flask test client | `tests/test_app.py` |
| End-to-end UI | Real user flows in a browser | Selenium WebDriver, Page Object Model | `tests/ui/` |
| Manual | Exploratory and scripted checks | Test cases in `docs/test_cases.csv` | Browser |

Test design techniques:
- **Boundary Value Analysis:** every grade boundary (e.g. 79.99, 80, 100) and marks limits (-1, 0, 100, 101).
- **Equivalence Partitioning:** one representative value from each grade band and each class of invalid input.
- **Negative testing:** empty fields, wrong password, non-numeric and out-of-range marks, duplicate roll.

## 4. Test environment

| Environment | Details |
|---|---|
| OS | Windows 10/11 (local); Ubuntu and Windows (GitHub Actions) |
| Browser | Google Chrome (latest), headless and headed |
| Python | 3.10, 3.11, 3.12 |
| Test data | Fresh SQLite database created for every test |

## 5. Entry criteria
- Application starts and the login page loads
- Test cases reviewed

## 6. Exit criteria
- All planned test cases executed
- Every failed test has a bug report
- No open Critical or High severity bugs

## 7. Deliverables
- Test cases (`docs/test_cases.csv`) with Actual Result and Status filled in
- Automated test report (`report.html`)
- Bug reports (`docs/bug_reports/` or Jira)
- Test summary (in README)

## 8. Risks
| Risk | Mitigation |
|---|---|
| Browser and driver version mismatch breaks UI tests | Selenium Manager downloads the matching driver automatically |
| Grading rules misunderstood | The grading table in `app/grading.py` is the single source of truth |
