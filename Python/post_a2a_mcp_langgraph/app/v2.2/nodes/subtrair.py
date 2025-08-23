from schema.calc_state import CalcState

def subtrair(state: CalcState) -> CalcState:
    return {**state, "result": state["num1"] - state["num2"]}