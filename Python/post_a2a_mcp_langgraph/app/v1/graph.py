from agents import graph

def save_graph_image(graph, filename="agent_graph_v1.png"):
    try:
        img_data = graph.get_graph().draw_mermaid_png()
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Grafo salvo com sucesso em '{filename}'")
    except Exception as e:
        print("Erro ao salvar grafo:", e)

if __name__ == "__main__":
    print("Gerando imagem do grafo...")
    save_graph_image(graph)
