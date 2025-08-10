from fastmcp import FastMCP

mcp = FastMCP("Math 🚀")

@mcp.tool
def somar(a, b):
    """Soma dois números."""
    return a + b


@mcp.tool
def subtrair(a, b):
    """Subtrai dois números"""
    return a - b


@mcp.tool
def multiplicar(a, b):
    """Multiplica dois números."""
    return a * b


if __name__ == "__main__":
    print("\n🚀 Starting  Server...")
    mcp.run(transport="http", host="0.0.0.0", port=8000)