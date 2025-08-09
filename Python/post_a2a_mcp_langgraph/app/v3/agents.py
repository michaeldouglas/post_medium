from langgraph.graph.state import StateGraph, START, END

from schema import CalcState     
from nodes import decisor, decide_operacao, somar, subtrair, multiplicar, exibir_resultado

workflow = StateGraph(CalcState)

workflow.add_node("decisor", decisor)
workflow.add_node("somar", somar)
workflow.add_node("subtrair", subtrair)
workflow.add_node("multiplicar", multiplicar)
workflow.add_node("exibir_resultado", exibir_resultado)

workflow.add_edge(START, "decisor")
workflow.add_conditional_edges("decisor", decide_operacao)
workflow.add_edge("somar", "exibir_resultado")
workflow.add_edge("subtrair", "exibir_resultado")
workflow.add_edge("multiplicar", "exibir_resultado")
workflow.add_edge("exibir_resultado", END)

graph = workflow.compile()
