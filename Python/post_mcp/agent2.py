"""Agente langchain mcp"""
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

client = MultiServerMCPClient({
    "mcpstore": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http"
    }
})


def agent2(query: str):
    """Execução do agente"""
    tools = asyncio.run(client.get_tools())

    prompt = (
        "Você é um agente especializado em previsão do tempo e hora local. "
        "Responda apenas perguntas relacionadas a clima e hora local, "
        "e recuse-se a outras."
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt
    )

    response = asyncio.run(agent.ainvoke({"messages": query}))
    return response


if __name__ == "__main__":
    PERGUNTA = "Qual a previsão do tempo e a hora local para Curitiba?"
    RESPOSTA = agent2(PERGUNTA)
    print(RESPOSTA["messages"][-1].content)
