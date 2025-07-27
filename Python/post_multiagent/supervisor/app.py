import logging
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.schemas import ChatRequest
from src.agents import compiled_app
from src.utils import extrair_resposta_final
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message:
        return JSONResponse(status_code=400, content={"error": "Campo 'message' é obrigatório"})
    try:
        logger.info(f"Mensagem recebida no /chat: {payload.message}")
        result = compiled_app.invoke({
            "messages": [{"role": "user", "content": f"{payload.message} session_id: {payload.session_id} client_id: {payload.client_id}"}]
        })
        resposta = extrair_resposta_final(result)
        logger.info(f"Resposta gerada: {resposta}")
        return {"resposta": resposta}
    except Exception as e:
        logger.exception("Erro ao processar requisição no endpoint /chat")
        return JSONResponse(status_code=500, content={"error": str(e)})
