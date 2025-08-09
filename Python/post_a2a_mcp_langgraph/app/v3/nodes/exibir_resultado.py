from schema.calc_state import CalcState

def exibir_resultado(state: CalcState) -> CalcState:
    mensagem = f"A sua conta deu: {state['result']}"
    return {**state, "mensagem": mensagem}