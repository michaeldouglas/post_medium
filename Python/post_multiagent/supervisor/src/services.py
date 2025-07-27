import requests
import logging

logger = logging.getLogger(__name__)

def consultar_saldo_remoto(message: str) -> str:
    """Consulta o saldo bancário de um cliente"""

    url = "http://balance_agent:8000/saldo"
    payload = {"message": message}
    try:
        logger.info(f"➡️ Enviando requisição SALDO para {url} com payload: {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Resposta SALDO recebida: {data}")
        return data.get("resposta", "Resposta não encontrada.")
    except Exception as e:
        logger.exception("❌ Erro ao consultar saldo remoto")
        return f"Erro ao consultar saldo remoto: {str(e)}"

def consultar_cartao_remoto(message: str) -> str:
    """Consulta o cartão de crédito de um cliente via agente remoto"""
     
    url = "http://card_agent:8000/cartao"
    payload = {"message": message}
    try:
        logger.info(f"Enviando requisição CARTÃO para {url} com payload: {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Resposta CARTÃO recebida: {data}")
        return data.get("resposta", "Resposta não encontrada.")
    except Exception as e:
        logger.exception("Erro ao consultar cartão remoto")
        return f"Erro ao consultar cartão remoto: {str(e)}"
