from schema.faq_state import FaqState


def validar_intencao(state: FaqState) -> FaqState:
    """Valida a intenção do usuário."""
    state.resposta = f"Intenção '{state.intencao}' reconhecida com sucesso!"
    return state
