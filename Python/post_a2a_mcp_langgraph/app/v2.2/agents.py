from langgraph.graph.state import StateGraph, START, END

from schema import CalcState     
from nodes import decisor, decide_operacao, somar, subtrair, multiplicar

workflow = StateGraph(CalcState)

workflow.add_node("decisor", decisor)
workflow.add_node("somar", somar)
workflow.add_node("subtrair", subtrair)
workflow.add_node("multiplicar", multiplicar)

workflow.add_edge(START, "decisor")
workflow.add_conditional_edges("decisor", decide_operacao)
workflow.add_edge("somar", END)
workflow.add_edge("subtrair", END)
workflow.add_edge("multiplicar", END)

graph = workflow.compile()
