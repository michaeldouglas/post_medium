from schema.calc_state import CalcState
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def exibir_resultado(state: CalcState) -> CalcState:
    logging.info(f"Executando exibir_resultado com estado: {state}")

    try:
        mensagem = f"A sua conta deu: {state['result']}"
    except Exception as e:
        logging.error(f"Erro ao exibir resultado: {e}")
        mensagem = "Erro ao exibir resultado"
    finally:
        state["finished_at"] = datetime.utcnow().isoformat()
    
    return {**state, "mensagem": mensagem}