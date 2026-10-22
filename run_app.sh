#!/usr/bin/env bash
# Start the app for manual testing (macOS/Linux)
cd "$(dirname "$0")"
[ -d .venv ] || { python3 -m venv .venv; source .venv/bin/activate; pip install -q -r requirements.txt; }
source .venv/bin/activate
echo "App running at http://127.0.0.1:5000  (login: admin / admin123)"
python -m app.main
