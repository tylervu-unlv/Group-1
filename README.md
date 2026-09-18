# Group-1

[![CI Workflow](https://github.com/tylervu-unlv/Group-1/actions/workflows/ci.yml/badge.svg)](https://github.com/tylervu-unlv/Group-1/actions/workflows/ci.yml)

## Continuous Integration

This repository runs an automated CI workflow (`.github/workflows/ci.yml`) on every push and pull request. The workflow:

- Runs the test suite (`pytest --cov=src --cov-report=term-missing`) against Python 3.9, 3.10, and 3.11 to ensure compatibility across versions.
- Runs Flake8 linting (`flake8 src --select=E9,F63,F7,F82`) to catch critical syntax and logic errors.

### Investigating a failed check

If the CI badge above shows failing, or a pull request shows a red ❌ on its checks:

1. Go to the **Actions** tab in this repository.
2. Click the failing workflow run.
3. Expand the failed step (e.g., "Run Tests with Pytest" or "Run Flake8 Linting") to see the full error output.
4. Common causes:
   - A test assertion failed — check the pytest output for which test and why.
   - A linting error was introduced — Flake8's output shows the exact file and line.
5. Fix the issue locally, re-run `pytest --cov=src` (or `flake8 src`) to confirm it passes, then push the fix — CI will automatically re-run.
