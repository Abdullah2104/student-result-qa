"""End-to-end UI tests with Selenium WebDriver (Chrome).

Run only these:   pytest -m ui
Watch the browser: pytest -m ui --headed
"""
import pytest

from tests.ui.pages import AddStudentPage, LoginPage, ResultPage, StudentsPage

pytestmark = pytest.mark.ui


@pytest.fixture
def logged_in_browser(driver, live_server):
    LoginPage(driver, live_server).open().login("admin", "admin123")
    return driver


def test_UI01_login_success(driver, live_server):
    LoginPage(driver, live_server).open().login("admin", "admin123")
    assert StudentsPage(driver, live_server).heading() == "Students"


def test_UI02_login_wrong_password_shows_error(driver, live_server):
    page = LoginPage(driver, live_server).open()
    page.login("admin", "wrongpass")
    assert page.error_text() == "Invalid username or password"


def test_UI03_add_student_appears_in_list(logged_in_browser, live_server):
    AddStudentPage(logged_in_browser, live_server).open().fill_and_save("501", "Nadia", 88, 76, 91)
    assert "501" in StudentsPage(logged_in_browser, live_server).rolls()


def test_UI04_marks_above_100_show_error(logged_in_browser, live_server):
    page = AddStudentPage(logged_in_browser, live_server).open()
    page.fill_and_save("502", "Test", 120, 50, 50)
    assert "Bangla: Marks must be between 0 and 100" in page.errors()


def test_UI05_result_page_shows_grade(logged_in_browser, live_server):
    AddStudentPage(logged_in_browser, live_server).open().fill_and_save("503", "Sumi", 70, 72, 74)
    result = ResultPage(logged_in_browser, live_server).open("503")
    assert result.average() == "72.0"
    assert result.grade() == "A-"


def test_UI06_negative_marks_show_error(logged_in_browser, live_server):
    page = AddStudentPage(logged_in_browser, live_server).open()
    page.fill_and_save("504", "Negative", -10, 50, 50)
    assert "Bangla: Marks must be between 0 and 100" in page.errors(), "negative marks were accepted"
