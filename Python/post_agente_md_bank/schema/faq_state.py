from typing import Optional
from pydantic import BaseModel
from langchain.messages import AnyMessage


class FaqState(BaseModel):
    """Estado do agente de FAQ com mensagens do LLM."""
    messages: list[AnyMessage]  # aqui armazenamos histórico do chat
    intencao: str = "outro"
    nome_cliente: Optional[str] = None
    resposta: Optional[str] = None
