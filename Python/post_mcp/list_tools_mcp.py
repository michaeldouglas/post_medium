"""List Tool MCP"""
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient


async def list_tools():
    client = MultiServerMCPClient({
        "mcpstore": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    })
    tools = await client.get_tools()
    for tool in tools:
        print(f"Nome da ferramenta: {tool.name}")
        print(f"Descrição: {tool.description}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(list_tools())
