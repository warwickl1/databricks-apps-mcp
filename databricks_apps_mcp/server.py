from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom MCP Server on Databricks Apps")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a (int): First number to be added
        b (int): Second number to be added

    Returns:
        int: The sum of the two numbers
    
    """
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers.

    Args:
        a (int): The number to be subtracted from
        b (int): The number to subtract

    Returns:
        int: The result of the subtraction
    
    """
    return a - b

mcp_app = mcp.streamable_http_app()


app = FastAPI(lifespan=lambda _: mcp.session_manager.run())
app.mount("/", mcp_app)
