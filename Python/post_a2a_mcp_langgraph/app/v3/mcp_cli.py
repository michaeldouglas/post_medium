import asyncio
from fastmcp import Client

# HTTP server
client = Client("http://localhost:8000/mcp")

async def main():
    async with client:
        # Valida a conexão com o servidor
        await client.ping()
        
        # Lista as ferramentas disponíveis
        tools = await client.list_tools()
        
        # Exibe
        print("Exibindo ferramentas disponíveis:")
        for tool in tools:
            print(f"- {tool.name}")
        print("\n-----------------------------------------\n")

        # Execute operations
        result = await client.call_tool("somar", {"a": 5, "b": 10})
        valor = result.content[0].text
        print("Resultado da soma:")
        print(valor)

        print("\n-----------------------------------------\n")
        result = await client.call_tool("subtrair", {"a": 10, "b": 5})
        valor = result.content[0].text
        print("Resultado da subtração:")
        print(valor)

        print("\n-----------------------------------------\n")
        result = await client.call_tool("multiplicar", {"a": 2, "b": 2})
        valor = result.content[0].text
        print("Resultado da multiplicação:")
        print(valor)

asyncio.run(main())