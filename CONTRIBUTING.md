# 🤝 Contributing to AnalisiOpenData
| | | |
|-|-|-|
| 0 | [![Contributing](https://img.shields.io/badge/Contributing-663399?style=plastic&logo=github&logoColor=white)](CONTRIBUTING.md) | *Contributions are welcome! Follow these guidelines:* | 
| 1 | [![Open an Issue](https://img.shields.io/badge/Open_an_Issue-FF5252?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/issues) | *Verify that it has not already been reported, describe the problem with examples* |
| 2 | [![Submit a PR](https://img.shields.io/badge/Submit_a_PR-4CAF50?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/pulls) | *Fork, create a branch, make sure tests pass* |
| 4 | [![Docs](https://img.shields.io/badge/Update-Docs-0288D1?style=plastic&logo=readthedocs&logoColor=white)](CONTRIBUTING.md) | *Update documentation* |
| 3 | [![Coding Standards](https://img.shields.io/badge/Coding_Standards-PEP8-0288D1?style=plastic&logo=python&logoColor=white)](CONTRIBUTING.md) | *Follow PEP8 for Python* |
| 5 | [![Pull Requests](https://img.shields.io/badge/Pull_Requests-4CAF50?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/pulls) | Process of pull requests |
| 6 | [![Discussions](https://img.shields.io/badge/Discussions-Q%26A_%26_Proposals-0288D1?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/discussions) | *Open a discussion for questions or proposals* |

*Thank you for your interest in contributing to AnalisiOpenData! This document provides guidelines for contributing to the project effectively.*

---

## 🐛[![Report Issues](https://img.shields.io/badge/Report_Issues-FF5252?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/issues)

**Before opening an issue:**

1. **Check** that the bug has not already been reported in existing [issues](https://github.com/1ESA1/AnalisiOpenData/issues)
2. **Update** to the latest version of the project

**How to report:**

Open a new issue with the "Bug Report" template and include:

- **Clear description** of the problem
- **Steps to play** the bug
- **Expected Behavior** vs **Actual Behavior**
- **Screenshot** or **log** (if relevant)
- **Python Version** and Dependencies

---

## 💡[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-4CAF50?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/pulls)

**Before proposing a new feature:**

1. **Check** that it has not already been requested in the [issue](https://github.com/1ESA1/AnalisiOpenData/issues)
2. **Open a discussion** to propose the idea and receive feedback

**How to propose:**

Open a new issue with the "Feature Request" template and include:

- **Description** of the functionality
- **Motivation** (why is it useful?)
- **Possible implementation** (if you already have an idea)

---

## 📐[![Coding Standards](https://img.shields.io/badge/Coding_Standards-PEP8_%26_Docs-0288D1?style=plastic&logo=python&logoColor=white)](CONTRIBUTING.md)

- **Python**: Follow [![PEP8](https://img.shields.io/badge/PEP8-0288D1?style=plastic&logo=python&logoColor=white)](https://peps.python.org/pep-0008/) for code styling
- **Docstring**: Use the **Google** or **NumPy** format to document functions and classes
- **Comments**: Write comments in **English** to explain complex logic
- **Names**: Use descriptive names for variables and functions (e.g. 'get_dataset_list()')
- **Line Length**: Maximum 79 characters for code, 72 for comments

**Docstring Example:**

```python
def analyze_accidents(data: pd.DataFrame) -> dict:
    """
    Analyzes road accident data and returns statistics.

    Args:
        data (pd.DataFrame): DataFrame containing accident data
            with columns: 'latitudine', 'longitudine', 'data'

    Returns:
        dict: Dictionary with 'total_accidents', 'date_range', 'map_html'
    """
    pass
```

## 🧪 [![Testing](https://img.shields.io/badge/Run_Tests-6DB33F?style=plastic&logo=testing-library&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/tests)

Before sending a Pull Request:

Run all tests to check for regressions:

```bash
cd tests
python run_unified_tests.py
```

Add tests for new features or fixes:

Tests go to the tests/folder

Follow the format of existing tests

Make sure all tests pass

Specific tests:

```bash
python test_config.py      # Configuration
python test_unified.py     # Unit Test
python test_utils.py       # Utility
```

🔄[![Pull Requests](https://img.shields.io/badge/Pull_Requests-4CAF50?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/pulls)

Step 1: Fork and Clone
```bash
# Repository fork on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/AnalisiOpenData.git
cd AnalysisOpenData
```

Step 2: Create a Branch
```bash
git checkout -b feature/feature-name
# or
git checkout -b fix/bug-name
```

Step 3: Make the Changes
Follow the Coding Standards

Add tests for new features

Update documentation if necessary

Step 4: Commit and Push

```bash
git add.
git commit -m "Clear description of changes"
git push origin feature/feature-name
```
Step 5: Open the Pull Request

Go to the original repository on GitHub

Click on "Compare & pull request"

Fill in the template:

Description: What you did and why

Linked issue: If it resolves an issue, link it (e.g. "Fixes #123")

Test: Specify which tests you performed

What to expect
A maintainer will review the PR within 1-2 weeks

Changes may be required

Once approved, it will be merged into the main branch

[![Discussions](https://img.shields.io/badge/Discussions-Q%26A_%26_Proposals-0288D1?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData/discussions) *Open a Discussion in the GitHub Discussions section, Do not use issues for generic questions*

[![License](https://img.shields.io/badge/License-Apache%202.0-5C2D91?style=plastic&logo=apache&logoColor=white)](LICENSE) *By contributing to this project, you agree that your contributions are distributed under the Apache License 2.0.*

[![GitHub](https://img.shields.io/badge/GitHub-1ESA1-181717?style=plastic&logo=github&logoColor=white)](https://github.com/1ESA1) *Contact the maintainer, for urgent questions*

[![Docs](https://img.shields.io/badge/Documentation-4CAF50?style=plastic&logo=readthedocs&logoColor=white)](https://github.com/1ESA1/AnalisiOpenData) *Thank you for your contribution!*
