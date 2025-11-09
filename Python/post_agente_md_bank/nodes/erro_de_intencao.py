from schema.faq_state import FaqState


def erro_de_intencao(state: FaqState) -> FaqState:
    """Trata erro de intenção não reconhecida."""
    state.resposta = (
        "Desculpe, não consegui entender sua intenção.\n"
        "Por favor, escolha uma das opções: "
        "cartao_de_credito, conta_corrente, emprestimo ou investimentos."
    )
    return state
