from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class MathState(TypedDict):
    operacao: str # "somar", "subtrair", "multiplicar"
    dados: tuple[int, int]
    resultado: Annotated[str, add_messages]

graph_builder = StateGraph(MathState)

# Nó decisor: decide qual operação executar
def decisor(state: MathState):
    op = state["operacao"].lower()
    if op in ("somar", "subtrair", "multiplicar"):
        # Retorna o nome do próximo nó a ser executado
        return {"next_node": op}
    else:
        raise ValueError(f"Operação desconhecida: {op}")

# Nós das operações
def somar_node(state: MathState):
    a, b = state["dados"]
    return {"resultado": [{"role": "assistant", "content": str(a + b)}]}

def subtrair_node(state: MathState):
    a, b = state["dados"]
    return {"resultado": [{"role": "assistant", "content": str(a - b)}]}

def multiplicar_node(state: MathState):
    a, b = state["dados"]
    return {"resultado": [{"role": "assistant", "content": str(a * b)}]}

# Adiciona nós ao grafo
graph_builder.add_node("decisor", decisor)
graph_builder.add_node("somar", somar_node)
graph_builder.add_node("subtrair", subtrair_node)
graph_builder.add_node("multiplicar", multiplicar_node)

# Liga START ao decisor
graph_builder.add_edge(START, "decisor")

# Liga decisor aos nós possíveis SEM condição
graph_builder.add_edge("decisor", "somar")
graph_builder.add_edge("decisor", "subtrair")
graph_builder.add_edge("decisor", "multiplicar")

# Liga cada nó de operação ao END
graph_builder.add_edge("somar", END)
graph_builder.add_edge("subtrair", END)
graph_builder.add_edge("multiplicar", END)

# Compila o grafo
graph = graph_builder.compile()
