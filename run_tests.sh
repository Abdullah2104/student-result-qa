#!/usr/bin/env bash
# One-click (macOS/Linux): set up, run ALL tests, write report.html
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
pytest --html=report.html --self-contained-html || true
echo "Test report saved as report.html"
