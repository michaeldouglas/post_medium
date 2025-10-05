import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.schemas.chat import ChatRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/chat",
    tags=["Chat"],
    summary="Enviar mensagem para o chat",
    response_description="Retorna a resposta do chat",
)
def chat_endpoint(payload: ChatRequest):
    """
    Recebe um JSON com a mensagem do usuário e retorna uma resposta simulada.

    ### Request Example:
    ```json
    {
        "user": "Michael",
        "message": "Olá, tudo bem?"
    }
    ```

    ### Response Example:
    ```json
    {
        "reply": "Olá, Michael! Tudo ótimo!"
    }
    ```
    """
    logger.info(f"Mensagem recebida {payload.message}")
    return JSONResponse(content={"reply": f"Olá Tudo ótimo!"})
