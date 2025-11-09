from typing import Literal
from schema.faq_state import FaqState


def chegar_intencao_do_cliente(
    state: FaqState,
) -> Literal["validar_intencao", "erro_de_intencao"]:
    """Decide para qual nó seguir com base na intenção detectada."""
    validas = ["cartao_de_credito", "conta_corrente",
               "emprestimo", "investimentos"]
    return "validar_intencao" if state.intencao in validas else "erro_de_intencao"
