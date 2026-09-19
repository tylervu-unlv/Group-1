# **📌 Continuous Integration (CI) Lab**
Welcome to the **CI Lab**! In this lab, you will extend your work from the Testing Lab by setting up a **Continuous Integration (CI) pipeline** using **GitHub Actions**. This pipeline will automatically run tests and enforce code quality whenever changes are pushed to the repository.

---

## **📌 Lab Objectives**
By completing this lab, you will:
✅ Configure **GitHub Actions** to run automated tests on every commit and pull request.  
✅ Extend test coverage by writing **additional test cases**.  
✅ Implement **linting** to enforce code quality.  
✅ Learn how to **troubleshoot failed CI builds**.  
✅ Collaborate effectively by reviewing and merging **Pull Requests (PRs)**.  

---

## **📌 Getting Started**

### **1. Copy the Files into Your Team Repository**

Copy the lab files into a folder named **`ci_lab`** (underscore, not hyphen) in your team repository. The workflow declares `working-directory: ci_lab`, so any other spelling breaks the build.

```bash
cp -r * /path/to/your/team/repository/ci_lab/
cd /path/to/your/team/repository/ci_lab/
```

Do **not** copy this repository's `.git/` directory.

### **2. Move `ci.yml` to the Repository Root**

> ⚠️ **This is the step most teams get wrong.** GitHub Actions only runs workflows found in `.github/workflows/` **at the root of the repository**. A workflow file left inside `ci_lab/` is never executed.

`ci.yml` ships at the top level of *this* repository, but it belongs at the root of *your team* repository:

```text
<team-repo-root>/
├── .github/
│   └── workflows/
│       └── ci.yml        <-- the workflow lives here
└── ci_lab/               <-- the application code lives here
    ├── requirements.txt
    ├── pytest.ini
    ├── src/
    └── tests/
```

### **3. Python Version(s)**

You need Python **3.9 or later**. The lab has been tested on `3.9.6` and `3.13.5`. The workflow itself runs Python 3.9 by default.

### **4. Create a Virtual Environment and Install Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### **5. Run the Tests Locally**

Always confirm the suite is green locally before pushing — a failing local run will fail in CI too.

```bash
pytest --cov=src --cov-report=term-missing
```

All **22** tests should pass at roughly **95%** coverage.

### **6. Run the Linters Locally** *(needed for the lint/format enhancement)*

`flake8` and `black` are not runtime dependencies, so they live in a separate file:

```bash
pip install -r requirements-dev.txt

flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics   # what CI runs today
flake8 src tests --count                                               # full strength
black --check .
```

The workflow's Flake8 step currently selects only a few error classes, which the starter code passes. A full-strength run reports considerably more, and `black --check` would reformat several files — deciding what to do about that is part of the lint enhancement.

## **📂 Lab Overview**
In this lab, you will:  
✔️ Set up **GitHub Actions** for Continuous Integration.  
✔️ Automate running **test cases** on every **push** and **pull request**.  
✔️ Enforce **code quality checks** using **Flake8** for Python linting.  
✔️ Extend **test coverage** by adding **new test cases**.  
