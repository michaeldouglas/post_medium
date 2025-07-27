from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import os

load_dotenv()

app = FastAPI()

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

def consultar_cartao(cliente_id: str) -> str:
    """Consulta o cartão de crédito de um cliente"""
    cartoes_fake = {
        "cliente123": {"limite": 5000.00, "fatura": 1200.50},
        "cliente456": {"limite": 3000.00, "fatura": 800.00},
        "cliente789": {"limite": 2000.00, "fatura": 1500.00},
    }
    info = cartoes_fake.get(cliente_id)
    if not info:
        return f"Cliente {cliente_id} não possui cartão de crédito cadastrado."
    return (
        f"Cliente {cliente_id} tem limite de cartão de crédito de R$ {info['limite']:.2f} "
        f"e fatura atual de R$ {info['fatura']:.2f}."
    )

cartao_agent = create_react_agent(
    model=model,
    tools=[consultar_cartao],
    name="cartao_expert",
    prompt="Você é um especialista bancário que responde dúvidas sobre cartão de crédito."
)

class MensagemRequest(BaseModel):
    message: str

def extrair_resposta_final(result):
    mensagens = result.get("messages", [])
    respostas = [
        m.content for m in mensagens
        if isinstance(m, AIMessage) and m.content and "Transferring back" not in m.content
    ]
    return respostas[-1] if respostas else "Nenhuma resposta encontrada."

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/cartao")
async def consultar_cartao_endpoint(request: MensagemRequest):
    mensagem = request.message
    if not mensagem:
        return JSONResponse(status_code=400, content={"error": "Campo 'message' obrigatório"})

    try:
        result = cartao_agent.invoke({
            "messages": [{"role": "user", "content": mensagem}]
        })
        resposta = extrair_resposta_final(result)
        return {"resposta": resposta}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
