from langgraph.graph import StateGraph, START, END
from schema.faq_state import FaqState
from nodes.receber_mensagem import receber_mensagem
from nodes.validar_intencao import validar_intencao
from nodes.erro_de_intencao import erro_de_intencao
from nodes.conditions.chegar_intencao_do_cliente import chegar_intencao_do_cliente
from nodes.resultado import resultado


def create_workflow():
    """Cria o grafo do agente de FAQ."""
    workflow = StateGraph(FaqState)

    workflow.add_node("receber_mensagem", receber_mensagem)
    workflow.add_node("validar_intencao", validar_intencao)
    workflow.add_node("erro_de_intencao", erro_de_intencao)
    workflow.add_node("resultado", resultado)  # novo node

    workflow.add_edge(START, "receber_mensagem")
    workflow.add_conditional_edges(
        "receber_mensagem", chegar_intencao_do_cliente)

    # Após validar_intencao ou erro_de_intencao, vai para resultado
    workflow.add_edge("validar_intencao", "resultado")
    workflow.add_edge("erro_de_intencao", "resultado")

    # resultado finaliza o workflow
    workflow.add_edge("resultado", END)

    return workflow.compile()
