from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
import os
from dotenv import load_dotenv
from src.services import consultar_saldo_remoto, consultar_cartao_remoto

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

saldo_agent = create_react_agent(
    model=model,
    tools=[consultar_saldo_remoto],
    name="saldo_expert",
    prompt="Você é um especialista bancário que responde sobre saldo bancário consultando um serviço externo."
)

cartao_agent = create_react_agent(
    model=model,
    tools=[consultar_cartao_remoto],
    name="cartao_expert",
    prompt="Você é um especialista bancário que responde dúvidas sobre cartão de crédito consultando um serviço externo."
)

workflow = create_supervisor(
    [saldo_agent, cartao_agent],
    model=model,
    prompt=(
        "Você é o supervisor de dois agentes bancários: saldo_expert e cartao_expert. "
        "Para perguntas sobre saldo bancário, use saldo_expert. "
        "Para perguntas sobre cartão de crédito, use cartao_expert."
        "Você sempre deve usar as respostas dos agentes bancários e explicar de forma clara baseado no retorno deles"
    )
)

compiled_app = workflow.compile()
