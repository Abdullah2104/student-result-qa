"""Student Result Management System: the application under test.

Run:  python -m app.main     then open http://127.0.0.1:5000
Login: admin / admin123
"""
import os
import sqlite3
from functools import wraps

from flask import Flask, g, redirect, render_template, request, session, url_for

from app.grading import SUBJECTS, average, grade, validate_mark

USERNAME = "admin"
PASSWORD = "admin123"


def create_app(db_path=None):
    app = Flask(__name__)
    app.secret_key = "dev-only-secret"
    app.config["DB_PATH"] = db_path or os.environ.get("RESULT_DB", "results.db")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        db = get_db()
        db.execute(
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, roll TEXT, name TEXT, "
            "bangla INTEGER, english INTEGER, mathematics INTEGER)"
        )
        db.commit()

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user"):
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    @app.route("/")
    def index():
        return redirect(url_for("students"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            if not username or not password:
                error = "Username and password are required"
            elif username == USERNAME and password == PASSWORD:
                session["user"] = username
                return redirect(url_for("students"))
            else:
                error = "Invalid username or password"
        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/students")
    @login_required
    def students():
        rows = get_db().execute("SELECT * FROM students ORDER BY id").fetchall()
        return render_template("students.html", students=rows)

    @app.route("/students/add", methods=["GET", "POST"])
    @login_required
    def add_student():
        errors = []
        form = request.form
        if request.method == "POST":
            roll = form.get("roll", "").strip()
            name = form.get("name", "").strip()
            if not roll:
                errors.append("Roll is required")
            if not name:
                errors.append("Name is required")
            marks = {}
            for subject in SUBJECTS:
                try:
                    marks[subject] = validate_mark(form.get(subject.lower()))
                except ValueError as exc:
                    errors.append(f"{subject}: {exc}")
            if roll and get_db().execute("SELECT 1 FROM students WHERE roll = ?", (roll,)).fetchone():
                   errors.append("Roll already exists")
            if not errors:
                db = get_db()
                db.execute(
                    "INSERT INTO students (roll, name, bangla, english, mathematics) VALUES (?, ?, ?, ?, ?)",
                    (roll, name, marks["Bangla"], marks["English"], marks["Mathematics"]),
                )
                db.commit()
                return redirect(url_for("students"))
        return render_template("add_student.html", errors=errors, form=form, subjects=SUBJECTS)

    @app.route("/students/<roll>")
    @login_required
    def result(roll):
        row = get_db().execute("SELECT * FROM students WHERE roll = ?", (roll,)).fetchone()
        if row is None:
            return render_template("not_found.html", roll=roll), 404
        marks = [row["bangla"], row["english"], row["mathematics"]]
        avg = average(marks)
        letter, point = grade(avg)
        return render_template("result.html", s=row, marks=dict(zip(SUBJECTS, marks)),
                               avg=avg, letter=letter, point=point)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
