import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API do chat",
    description="""
API para testar integração de chat e geração de boletos.

### Funcionalidades: 
- Endpoint `/chat`: envia mensagens para o chat.
- Endpoint `/boleto`: gera boletos para produtos usando Itaú (PDF em Base64).
""",
    version="1.0.0",
    contact={
        "name": "Michael Douglas Barbosa Araujo",
        "email": "michaeldouglas010790@gmail.com",
        "url": "https://github.com/michaeldouglas",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"], summary="Verifica se a API está rodando")
async def root():
    return {"message": "API is running"}

app.include_router(chat.router)
