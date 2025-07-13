"""Agente langchain mcp smithery"""
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOpenAI(
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

SMITHERY_API_KEY = os.getenv("SMITHERY_API_KEY")
SMITHERY_URL = "https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp"

client = MultiServerMCPClient({
    "local": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http"
    },
    "smithery": {
        "url": f"{SMITHERY_URL}?api_key={SMITHERY_API_KEY}&profile=christian-beaver-R2vVRT",
        "transport": "streamable_http"
    }
})


def agente_internet(query: str):
    """Agente que une ferramentas locais + Smithery (busca web)"""
    tools = asyncio.run(client.get_tools())

    prompt = (
        "Você é um agente com acesso à internet e a dados locais.\n"
        "Use 'duckduckgo_search' para buscar informações na web.\n"
        "Use 'clima' e 'horario' para obter dados locais de cidades.\n"
        "Responda de forma clara e útil para humanos."
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt
    )

    response = asyncio.run(agent.ainvoke({"messages": query}))
    return response


if __name__ == "__main__":
    PERGUNTA = "Qual a previsão do tempo em São Paulo e o nome do prefeito atual de São Paulo?"
    RESPOSTA = agente_internet(PERGUNTA)
    print("\n Resposta final:\n")
    print(RESPOSTA["messages"][-1].content)
