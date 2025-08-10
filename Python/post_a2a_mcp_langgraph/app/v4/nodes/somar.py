from schema.calc_state import CalcState
from call_tool import call_mcp_tool
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

async def somar(state: CalcState) -> CalcState:
    logging.info(f"Executando somar com estado: {state}")

    try:
        resultado = await call_mcp_tool("somar", state["num1"], state["num2"])
    except Exception as e:
        logging.error(f"Erro ao executar somar: {e}")
        resultado = None
    finally:
        state["finished_at"] = datetime.utcnow().isoformat()

    return {**state, "result": resultado}
