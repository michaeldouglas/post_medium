from schema.faq_state import FaqState
from langchain.messages import AIMessage


def resultado(state: FaqState) -> FaqState:
    """
    Node final que gera a resposta para o usuário como AIMessage,
    para que seja visível no LangSmith.
    """
    if state.intencao == "outro":
        texto = f"""Desculpe, não entendi sua solicitação: 
        Porque eu sei apenas sobre esses assuntos: 
        - cartao_de_credito, 
        - conta_corrente, 
        - emprestimo, 
        - investimentos.
        
        Messages: '{state.messages}'
        """
    else:
        texto = f"Olá {state.nome_cliente or ''}! Aqui está a informação sobre '{state.intencao}'."

    state.resposta = texto

    ai_message = AIMessage(content=texto)
    if hasattr(state, "messages"):
        state.messages.append(ai_message)
    else:
        state.messages = [ai_message]

    return state
