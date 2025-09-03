# DSG Cirium Data Science Project Template  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Internal-red)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green)
![Documentation](https://img.shields.io/badge/Confluence-Documentation-blue)

> A production-ready project structure for Data Science projects at Cirium, designed to work both locally and in Databricks.


## 1. Before You Start

Make the following changes to customize this template for your new project:

1. Decide a short name for your project, in **snake_case**.  
   Examples: `"Emissions"` → `emissions`, `"True Seats"` → `true_seats`

2. Rename the following in your repo:
   - The `project_name/` folder in the root directory
   - The `bundle.name` variable in `databricks.yml`
   - The `project.name` and `tool.setuptools.packages` variables in `pyproject.toml`


## 2. Local Development Setup

This template uses [uv](https://github.com/astral-sh/uv) for managing the local environment.

1. Install uv by following [this guide](https://docs.astral.sh/uv/getting-started/installation/) (PyPI method recommended)

2. Create the virtual environment and install development dependencies:

```bash
uv sync --all-extras --dev
```

3. (Optional) Install pre-commit hooks for code quality:

```bash
pre-commit install
```

4. Create a new folder called `experiments/` in your project root to store experiment notebooks.


## 3. Databricks Setup

### a. Using Databricks UI (Sandbox)

- Use the **Git Folder** feature to clone your repo and edit as usual.
- When creating clusters, manually install packages defined in `pyproject.toml` (Databricks does not yet fully support this).
- Create a new `experiments/` folder to store experiment notebooks, consistent with local setup.

### b. Deploying with Databricks Asset Bundles (Staging/Production)

- GitHub Actions workflows for deployment are preconfigured.
- Request **Cluster Policy IDs** and **Service Principals** from the Data Dragons team.
- Deployment branches:
  - Push to `main` deploys to **staging**
  - Push to `release` deploys to **production**
- For jobs and workflows:
  - Create a `resources/` folder for Databricks job config files.
  - Create a `workflows/` folder for notebooks to be run.

> Example jobs and workflows are available in the ``Examples/`` folder. You may delete this folder after reviewing.


## 4. Project Structure

```
project_root/  
├── .github/workflows/      # GitHub Actions workflows  
├── project_name/           # Source code  
├── tests/                  # Test files  
├── .gitignore              # Git ignore file  
├── .pre-commit-config.yaml # Pre-commit configuration  
├── databricks.yml          # Databricks asset bundle config  
├── pyproject.toml          # Python project config  
└── README.md               # Project documentation  
```


## 5. Notes

- Python 3.10+ is recommended  
- Development follows PEP 8 style, enforced by pre-commit hooks  
- For questions, contact the Data Science team  
