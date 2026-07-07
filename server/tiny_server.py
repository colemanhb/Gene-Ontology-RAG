from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test")

@mcp.tool()
def hello():
    return "Hello!"

app = mcp.streamable_http_app()