from fastmcp import Client

MCP_URL = "http://localhost:8000/mcp"

async def call_mcp_tool(tool_name: str, a: float, b: float) -> str:
    client = Client(MCP_URL)
    async with client:
        await client.ping()
        result = await client.call_tool(tool_name, {"a": a, "b": b})
        return result.content[0].text