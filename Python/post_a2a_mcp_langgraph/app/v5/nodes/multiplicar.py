from schema.calc_state import CalcState
from call_tool import call_mcp_tool
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)

async def multiplicar(state: CalcState) -> CalcState:
    logging.info(f"Executando multiplicar com estado: {state}")

    try:
        resultado = await call_mcp_tool("multiplicar", state["num1"], state["num2"])
    except Exception as e:
        logging.error(f"Erro ao executar multiplicar: {e}")
        resultado = None
    finally:
        state["finished_at"] = datetime.now(timezone.utc).isoformat()

    return {**state, "result": resultado}