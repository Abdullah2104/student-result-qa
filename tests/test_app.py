"""Functional (integration) tests through the web app, without a browser.

Each test name matches a manual test case ID in docs/test_cases.csv.
"""
from tests.conftest import add_student


# ---------- Login ----------
def test_TC01_login_valid(client):
    resp = client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
    assert b"<h1>Students</h1>" in resp.data


def test_TC02_login_wrong_password(client):
    resp = client.post("/login", data={"username": "admin", "password": "wrong"})
    assert b"Invalid username or password" in resp.data


def test_TC03_login_empty_fields(client):
    resp = client.post("/login", data={"username": "", "password": ""})
    assert b"Username and password are required" in resp.data


def test_TC04_pages_need_login(client):
    resp = client.get("/students")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]


def test_TC05_logout(logged_in):
    logged_in.get("/logout")
    assert logged_in.get("/students").status_code == 302


# ---------- Add student ----------
def test_TC06_add_valid_student(logged_in):
    resp = add_student(logged_in, roll="101", name="Rahim")
    assert b"Rahim" in resp.data


def test_TC07_name_required(logged_in):
    resp = add_student(logged_in, name="")
    assert b"Name is required" in resp.data


def test_TC08_roll_required(logged_in):
    resp = add_student(logged_in, roll="")
    assert b"Roll is required" in resp.data


def test_TC09_marks_above_100_rejected(logged_in):
    resp = add_student(logged_in, mathematics="101")
    assert b"Marks must be between 0 and 100" in resp.data


def test_TC10_negative_marks_rejected(logged_in):
    resp = add_student(logged_in, roll="102", bangla="-5")
    assert b"Marks must be between 0 and 100" in resp.data, "negative marks were accepted"


def test_TC11_non_numeric_marks_rejected(logged_in):
    resp = add_student(logged_in, english="abc")
    assert b"Marks must be a whole number" in resp.data


def test_TC12_duplicate_roll_rejected(logged_in):
    add_student(logged_in, roll="200", name="First")
    add_student(logged_in, roll="200", name="Second")
    listing = logged_in.get("/students")
    rows = listing.data.count(b'<td class="roll">200</td>')
    assert rows == 1, f"roll 200 appears {rows} times; duplicate roll was saved"


# ---------- Result ----------
def test_TC13_result_shows_correct_grade(logged_in):
    add_student(logged_in, roll="300", name="Karim", bangla="85", english="78", mathematics="90")
    resp = logged_in.get("/students/300")
    assert b'<span id="average">84.33</span>' in resp.data
    assert b'<span id="grade">A+</span>' in resp.data


def test_TC14_result_at_grade_boundary(logged_in):
    add_student(logged_in, roll="301", name="Boundary", bangla="80", english="80", mathematics="80")
    resp = logged_in.get("/students/301")
    assert b'<span id="grade">A+</span>' in resp.data, "average 80 should be A+"


def test_TC15_unknown_roll_returns_404(logged_in):
    resp = logged_in.get("/students/9999")
    assert resp.status_code == 404
