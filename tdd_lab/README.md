# 🧪 Test-Driven Development (TDD) Lab

## 📌 Overview
This lab focuses on **Test-Driven Development (TDD)**—writing test cases first and then implementing the required functionality. Each student will contribute **one test case** and submit a pull request.

---

## 📂 Project Structure

The repository is organized as follows:

```markdown
tdd_lab/
├── 📂 tests/                    # Contains all test cases
│   ├── 📄 __init__.py           # Marks tests as a package
│   ├── 📄 test_counter.py       # Test cases for the counter API (each student contributes a test)
├── 📂 src/                      # Source code for the counter service
│   ├── 📄 __init__.py           # Re-exports the Flask app and status codes
│   ├── 📄 counter.py            # Counter API implementation (starts out empty)
│   ├── 📄 status.py             # HTTP status codes
├── 📂 doc/                      # Supporting documentation
│   ├── 📄 mergeconflicts.md     # How to resolve conflicts in counter.py
├── 📄 requirements.txt          # Dependencies for the project
├── 📄 pytest.ini                # Pytest configuration
├── 📄 README.md                 # Project documentation
```

### Python Version(s)
To follow this lab, you need Python **version 3.9 or later**. The exercises have been tested on `3.9.6` and `3.13.5`, and any Python **3.9+** should work without configuration issues. Python 3.8 reached end of life in October 2024 and is no longer supported by the pinned dependencies.  

If you encounter any setup or configuration problems, please reach out to the **T.A.** for assistance.


### 1. Upgrading PIP:
Sometimes it is useful to upgrade `pip` before installing dependencies. If you like, run: `pip install --upgrade pip` and later install the dependencies using: `pip install -r requirements.txt`

### 2. Create a Virtual Environment (Highly Recommended)
 - It is a good practice to configure python virtual environment. Use the commands below to setup python virtual environment on `Linux/MacOS` or `Windows OS`
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
 ### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Set Flask Environment Variable
- macOS/Linux
```bash
   export FLASK_APP=src
```
- Windows
```bash
    set FLASK_APP=src
```
### 5. Run Flask Locally to Check Your Setup
```bash
flask run
```

Flask should start and report that it is serving on `http://127.0.0.1:5000`. A clean startup with no import errors is all you are checking here. Stop the server with `Ctrl+C`.

> ⚠️ **The starter app has no routes yet.** `src/counter.py` contains only a bare Flask app, so *every* URL — including `http://127.0.0.1:5000/counters/foo` — returns a generic **404 Not Found** page. That is the expected starting point: you add the endpoints yourself during the RED/GREEN cycle.

### 6. Verify the Test Setup
```bash
pytest --cov=src
```

`tests/test_counter.py` contains only a docstring at this point, so you should see a coverage table followed by:

```
============================ no tests ran in 0.02s =============================
```

pytest exits with **code 5** (`no tests collected`), and coverage prints `CoverageWarning: No data was collected`. Both are expected while the test file is still empty — neither is a setup failure.

### 7. Merge Conflicts
If you are having trouble merging changes to the main branch of the team's repo, you can take a look at this doc: [How to Handle Merge Conflicts in the Testing Lab](doc/mergeconflicts.md).


### 8. 🛠️ Troubleshooting Guide

Below are common errors students may encounter and their solutions:

| **Error** | **Cause** | **Solution** |
|-----------|----------|-------------|
| `ModuleNotFoundError: No module named 'src'` | Running from the wrong directory. `src/` must be in your current directory | `cd` into `tdd_lab/` before running `pytest` or `flask run` |
| `Error: Could not import 'src'.` | `flask run` started outside the lab folder, or `FLASK_APP` is unset | `cd` into `tdd_lab/`, then `export FLASK_APP=src` (macOS/Linux) or `set FLASK_APP=src` (Windows) |
| `ImportError: cannot import name 'app' from 'src'` | `src/counter.py` no longer defines `app` | Confirm `src/counter.py` still contains `app = Flask(__name__)` |
| `AttributeError: module 'src.status' has no attribute 'HTTP_400_BAD_REQUEST'` | `src/status.py` does not define a 400 constant | Add `HTTP_400_BAD_REQUEST = 400` to `src/status.py`, or use `from http import HTTPStatus`. Coordinate with your team — this file is shared |
| `404 Not Found` for every `/counters/...` URL | Expected before the endpoints exist | Not an error. Add the route during your GREEN phase |
| `no tests ran` / exit code `5` | `tests/test_counter.py` has no test functions yet | Expected before you write your first test |

If you continue to experience issues, follow these steps:
1. **Confirm you are in the `tdd_lab/` directory** — most import errors are a wrong-directory problem.
2. **Ensure all dependencies are installed** with `pip install -r requirements.txt`.
3. **Consult your team first before reaching out for help**.
4. **If the issue persists, open a GitHub Issue in your team repository**, including:
   - A clear description of the problem.
   - The exact error message.
   - Steps you have already tried.

🚀 **Debug first, then ask for help!**


