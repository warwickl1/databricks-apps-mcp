# Databricks Apps - MCP
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

> Example code for hosting a custom MCP serving using Databricks Apps.

Having a custom MCP server allows external users to interact with your data using Large Language Models. As a user of Databricks, we wanted to see if we could build our own (extremely basic) custom MCP server, host with Databricks Apps for our internal users, and allow them to "tap-in" to the tools we provide.

This example project uses Databricks Apps to host the server itself, and also provides a short example of how to interact with the server in Python on your local machine. For the LLM, it uses a model from the Databricks Model Serving endpoints. 

## How to use

### Host the Server

To host the server, run the following commands, replacing `<APP_NAME>` with your Databricks App name, and `<WORKSPACE_PATH>` with with your target workspace:

```bash
databricks sync . <WORKSPACE_PATH>
databricks apps deploy <APP_NAME> --source-code-path <WORKSPACE_PATH>
```

Once done, make sure your app is started, and check that the logs are all present and no errors have occurred.

## Connect using the client

Before running the client and interacting with the server, you must create a `.env` file with the following keys:
- `DATABRICKS_APP_URL`: Full URL pointing to your Databricks App. Example: `https/app-name-id.databricksapps.com/mcp`
- `DATABRICKS_MODEL_NAME`: Name of the model to use. Example: `databricks-gpt-oss-120b`
- `DATABRICKS_TOKEN`: Databricks PAT token. Starts with 'dapi'. Example: `dapi_7f9c2a1e8b4d6f3a9e2b`
- `DATABRICKS_ENDPOINTS_URL`: URl pointing to the serving endpoints in Databricks. Example: `https://workspace-environemnt.cloud.databricks.com/serving-endpoints/`

Once the environment variables are all set, you can run the client in your terminal using `uv`:

```bash
uv run databricks_apps_mcp/client.py
```

This will start an interactive terminal where the user can ask a single question, and the LLM will use the MCP server's tools to respond.

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
