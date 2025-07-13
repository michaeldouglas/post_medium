"""Servidor MCP"""
import requests
from fastmcp import FastMCP

mcp = FastMCP("API Simples de clima")


@mcp.tool
def clima(city: str) -> str:
    """Retorna a previsão do tempo para uma cidade."""
    response = requests.post(
        "http://localhost:9000/clima",
        json={"cidade": city},
        timeout=5
    )
    return response.json()["previsao"]


@mcp.tool
def horario(city: str) -> str:
    """Retorna a hora local para uma cidade."""
    response = requests.post(
        "http://localhost:9000/horario",
        json={"cidade": city},
        timeout=5
    )
    return response.json()["hora"]


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
