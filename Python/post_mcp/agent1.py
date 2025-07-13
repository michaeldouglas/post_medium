"""Agente langchain tools"""
import requests
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def clima(city: str) -> str:
    """Retorna a previsão do tempo para uma cidade."""
    response = requests.post(
        "http://localhost:9000/clima",
        json={"cidade": city},
        timeout=5
    )
    return response.json()["previsao"]


@tool
def horario(city: str) -> str:
    """Retorna a hora local para uma cidade."""
    response = requests.post(
        "http://localhost:9000/horario",
        json={"cidade": city},
        timeout=5
    )
    return response.json()["hora"]


model = ChatOpenAI(
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

tools = [clima, horario]

agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=(
        "Você é um agente especializado em previsão do tempo e hora local. "
        "Responda apenas perguntas relacionadas a clima e hora local, "
        "e recuse-se a outras."
    )
)

if __name__ == "__main__":
    result = agent.invoke({
        "messages": [
            HumanMessage(
                content="Qual a previsão do tempo e a hora local para Curitiba?")
        ]
    })
    print(result['messages'][-1].content)
