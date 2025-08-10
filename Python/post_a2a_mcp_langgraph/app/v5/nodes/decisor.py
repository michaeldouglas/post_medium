from typing import Literal
from schema.calc_state import CalcState
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)

def decisor(state: CalcState) -> CalcState:
    logging.info(f"Decidindo operação para: {state}")
    return {
        "num1": state["num1"], 
        "num2": state["num2"], 
        "operation": state["operation"], 
        "result": None,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }

def decide_operacao(state: CalcState) -> Literal["somar", "subtrair", "multiplicar"]:
    op = state.get("operation")
    logging.info(f"Operação escolhida: {op}")
    if op not in {"somar", "subtrair", "multiplicar"}:
        raise ValueError(f"Ops! A operação não é reconhecida. Por favor, escolha uma das seguintes operações: somar, subtrair ou multiplicar.")
    return op
