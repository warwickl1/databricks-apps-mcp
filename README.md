# Databricks Apps - MCP
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

> Example code for hosting a custom MCP serving using Databricks Apps.

Having a custom MCP server allows external users to interact with your data using Large Language Models. As a user of Databricks, we wanted to see if we could build our own (extremely basic) custom MCP server, host with Databricks Apps for our internal users, and allow them to "tap-in" to the tools we provide.

This example project uses Databricks Apps to host the server itself, and also provides a short example of how to interact with the server in Python on your local machine.


## Local Development Setup

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


## Notes

- Python 3.10+ is recommended  
- Development follows PEP 8 style, enforced by pre-commit hooks  
- For questions, contact the Data Science team at Cirium
