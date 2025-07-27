from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import re
import os

load_dotenv()

app = FastAPI()

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

def consultar_saldo(message: str) -> str:
    """Consulta o saldo bancário a partir da mensagem do usuário"""
    saldos_fake = {
        "cliente123": 2500.75,
        "cliente456": 1340.00,
        "cliente789": 980.20,
    }
    match = re.search(r"(cliente\d+)", message)
    if not match:
        return "Não consegui identificar o ID do cliente na sua pergunta."
    cliente_id = match.group(1)
    saldo = saldos_fake.get(cliente_id, 0.0)
    return f"O saldo disponível para o cliente {cliente_id} é R$ {saldo:.2f}"

saldo_agent = create_react_agent(
    model=model,
    tools=[consultar_saldo],
    name="saldo_expert",
    prompt="Você é um especialista bancário que responde perguntas sobre saldo bancário."
)

def extrair_resposta_final(result):
    mensagens = result.get("messages", [])
    respostas = [
        m.content for m in mensagens
        if isinstance(m, AIMessage) and m.content and "Transferring back" not in m.content
    ]
    return respostas[-1] if respostas else "Nenhuma resposta encontrada."

class ConsultaRequest(BaseModel):
    message: str

@app.post("/saldo")
async def consultar(request: ConsultaRequest):
    mensagem = request.message
    if not mensagem:
        raise HTTPException(status_code=400, detail="Campo 'message' obrigatório")
    try:
        result = saldo_agent.invoke({
            "messages": [{"role": "user", "content": mensagem}]
        })
        resposta = extrair_resposta_final(result)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health():
    return {"status": "ok"}
