import json
import os
from typing import cast

from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksOAuthClientProvider
from dotenv import load_dotenv
from mcp import Tool
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from rich.console import Console
from rich.rule import Rule

load_dotenv()


SYSTEM_PROMPT = "Use one of the tools whenever possible. If you cannot, say 'I cannot do that'. When giving the response after using a tool, please briefly explain your answer."

DATABRICKS_APP_URL = os.environ["DATABRICKS_APP_URL"]
DATABRICKS_MODEL_NAME = os.environ["DATABRICKS_MODEL_NAME"]
DATABRICKS_TOKEN = os.environ["DATABRICKS_TOKEN"]
DATABRICKS_ENDPOINTS_URL = os.environ["DATABRICKS_ENDPOINTS_URL"]


auth = DatabricksOAuthClientProvider( WorkspaceClient(profile="DEFAULT") )
client = OpenAI(api_key=DATABRICKS_TOKEN, base_url=DATABRICKS_ENDPOINTS_URL)
console = Console()


def to_openai_tool(tool: Tool) -> ChatCompletionToolParam:
    """Convert an MCP tool to an OpenAI tool."""
    return ChatCompletionToolParam(
        type="function",
        function={
            "name": tool.name,
            "description": tool.description or "Description not available.",
            "parameters": {
                "type": "object",
                "properties": { k: {"type": v["type"]} for k, v in tool.inputSchema["properties"].items() },
            },
            "strict": True,
        },
    )

def log_response(text: str) -> None:
    """Log the response to the console with proper formatting."""
    console.print(f"[red][Bot][/red] > [white]{text}")
    console.print(Rule(style="red"))

    
async def main() -> None:
    """Run the main loop of the program."""
    async with streamablehttp_client(DATABRICKS_APP_URL, auth=auth, terminate_on_close=False) as (read_stream, write_stream, _), ClientSession(read_stream, write_stream) as session:
        # Connect to the MCP server
        await session.initialize()
        
        # Grab a list of the tools (and convert them to OpenAI format)
        tools = [to_openai_tool(tool) for tool in (await session.list_tools()).tools]
        
        while True:
            # Get the user's input
            user_input = input("[You] > ")
            
            # Define the messages
            messages: list[ChatCompletionMessageParam] = [ {"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_input} ]

            # Get a response from the LLM
            response = client.chat.completions.create(model=DATABRICKS_MODEL_NAME, messages=messages, tools=tools)
            
            if response.choices[0].message.tool_calls is None:
                log_response("Sorry, there is no tool available to perform this task. Please try again with a different request.")
                continue
            
            tool_call = cast("list", response.choices[0].message.tool_calls)[0].function
            
            # Make the tool call
            mcp_response = str(((await session.call_tool(tool_call.name, json.loads(tool_call.arguments))).structuredContent or {}).get("result"))
            
            # Give the LLM the tool result to give a human response
            tooled_messages = [*messages, {"role": "assistant", "content": f"The tool returned: {mcp_response}."}]
            final_response = client.chat.completions.create(model=DATABRICKS_MODEL_NAME, messages=tooled_messages)
            
            # Print the LLMs response
            log_response(cast("list", final_response.choices[0].message.content)[-1]["text"])
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
