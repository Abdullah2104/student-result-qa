"""Page Object Model: one class per page, so tests read like user actions
and locators live in one place. If a button's id changes, only this file changes.

Every action that submits a form waits until the browser has loaded the next page
(explicit wait). Without this, a fast browser can move on before the server has
answered, and the test fails for a timing reason rather than a real defect.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_and_wait_for_new_page(driver, button, timeout=10):
    """Click a submit button and wait until the old page is gone (the next page has loaded)."""
    button.click()
    WebDriverWait(driver, timeout).until(EC.staleness_of(button))


class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")
    ERROR = (By.ID, "error")

    def __init__(self, driver, base_url):
        self.driver, self.base_url = driver, base_url

    def open(self):
        self.driver.get(f"{self.base_url}/login")
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        click_and_wait_for_new_page(self.driver, self.driver.find_element(*self.LOGIN_BTN))

    def error_text(self):
        return self.driver.find_element(*self.ERROR).text


class StudentsPage:
    HEADING = (By.TAG_NAME, "h1")
    ROLLS = (By.CSS_SELECTOR, "tr.student-row td.roll")
    ADD_LINK = (By.ID, "nav-add")

    def __init__(self, driver, base_url):
        self.driver, self.base_url = driver, base_url

    def heading(self):
        return self.driver.find_element(*self.HEADING).text

    def rolls(self):
        return [cell.text for cell in self.driver.find_elements(*self.ROLLS)]

    def go_to_add(self):
        self.driver.find_element(*self.ADD_LINK).click()


class AddStudentPage:
    SAVE_BTN = (By.ID, "save-btn")
    ERRORS = (By.CSS_SELECTOR, "p.error")

    def __init__(self, driver, base_url):
        self.driver, self.base_url = driver, base_url

    def open(self):
        self.driver.get(f"{self.base_url}/students/add")
        return self

    def fill_and_save(self, roll, name, bangla, english, mathematics):
        for field, value in [("roll", roll), ("name", name), ("bangla", bangla),
                             ("english", english), ("mathematics", mathematics)]:
            box = self.driver.find_element(By.ID, field)
            box.clear()
            box.send_keys(str(value))
        click_and_wait_for_new_page(self.driver, self.driver.find_element(*self.SAVE_BTN))

    def errors(self):
        self.driver.implicitly_wait(0)  # page is already loaded; don't wait when there are no errors
        try:
            return [e.text for e in self.driver.find_elements(*self.ERRORS)]
        finally:
            self.driver.implicitly_wait(3)


class ResultPage:
    def __init__(self, driver, base_url):
        self.driver, self.base_url = driver, base_url

    def open(self, roll):
        self.driver.get(f"{self.base_url}/students/{roll}")
        return self

    def grade(self):
        return self.driver.find_element(By.ID, "grade").text

    def average(self):
        return self.driver.find_element(By.ID, "average").text
