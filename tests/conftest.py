"""Shared pytest fixtures.

- `client`: Flask test client with a fresh database (fast, no browser).
- `logged_in`: the same client, already logged in as admin.
- `live_server` / `driver`: a real server on a free port plus a Chrome browser,
  used only by the Selenium tests in tests/ui/.
"""
import socket
import threading

import pytest
from werkzeug.serving import make_server

from app.main import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(db_path=str(tmp_path / "test.db"))


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})
    return client


def add_student(client, roll="101", name="Rahim", bangla="85", english="78", mathematics="90"):
    """Helper used by several tests: submit the Add student form."""
    return client.post("/students/add", data={
        "roll": roll, "name": name,
        "bangla": bangla, "english": english, "mathematics": mathematics,
    }, follow_redirects=True)


# ---------- Selenium (UI) fixtures ----------

def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="show the browser window during UI tests")


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def live_server(tmp_path):
    """Start the app on a free port in a background thread, with its own database."""
    app = create_app(db_path=str(tmp_path / "ui.db"))
    port = _free_port()
    server = make_server("127.0.0.1", port, app, threaded=True)  # threaded: Chrome opens extra idle connections that would block a single-threaded server
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture
def driver(request):
    """Chrome browser. Headless by default; pass --headed to watch it."""
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(3)
    yield browser
    browser.quit()
