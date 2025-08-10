from fastmcp import Client
import time
import logging

logging.basicConfig(level=logging.INFO)

MCP_URL = "http://localhost:8000/mcp"

async def call_mcp_tool(tool_name: str, a: float, b: float) -> str:
    client = Client(MCP_URL)
    async with client:
        start = time.time()

        await client.ping()

        logging.info(f"Chamando a função '{tool_name}' com parâmetros: a={a}, b={b}")
        result = await client.call_tool(tool_name, {"a": a, "b": b})
        elapsed = time.time() - start
        logging.info(f"Função '{tool_name}' retornou {result} em {elapsed:.3f}s")

        return result.content[0].text