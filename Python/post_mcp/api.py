"""API"""
import random
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CidadeRequest(BaseModel):
    """BaseModel Cidade"""
    cidade: str


@app.post("/clima")
def get_clima(data: CidadeRequest):
    """Obter previsão do tempo"""
    temp = round(random.uniform(18, 32), 1)
    return {"previsao": f"Tempo em {data.cidade}: {temp}°C com sol."}


@app.post("/horario")
def get_horario(data: CidadeRequest):
    """Obter horário"""
    now = datetime.now()
    return {"hora": f"Hora local em {data.cidade}: {now.strftime('%H:%M:%S')}"}
