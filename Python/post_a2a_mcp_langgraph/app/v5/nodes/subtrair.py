from schema.calc_state import CalcState
from call_tool import call_mcp_tool
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)

async def subtrair(state: CalcState) -> CalcState:
    logging.info(f"Executando subtrair com estado: {state}")

    try:
        resultado = await call_mcp_tool("subtrair", state["num1"], state["num2"])
    except Exception as e:
        logging.error(f"Erro ao executar subtrair: {e}")
        resultado = None
    finally:
        state["finished_at"] = datetime.now(timezone.utc).isoformat()

    return {**state, "result": resultado}