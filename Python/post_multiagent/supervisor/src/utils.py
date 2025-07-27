from langchain_core.messages import AIMessage

def extrair_resposta_final(result):
    mensagens = result.get("messages", [])
    respostas = [
        m.content for m in mensagens
        if isinstance(m, AIMessage) and m.content and "Transferring back" not in m.content
    ]
    return respostas[-1] if respostas else "Nenhuma resposta encontrada."
