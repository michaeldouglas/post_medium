import streamlit as st
import asyncio
from schema import CalcState
from graphs import graph

def run_graph_sync(state: CalcState):
    try:
        return asyncio.run(graph.ainvoke(state))
    except ValueError as e:
        return {"error": str(e), "messages": state.get("messages", [])}

def main():
    st.title("Agente Simples contas")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "resultado" not in st.session_state:
        st.session_state["resultado"] = ""

    user_input = st.text_input("Digite sua mensagem para o agente:")

    if st.button("Enviar") and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        state = CalcState(messages=st.session_state["messages"])

        result_state = run_graph_sync(state)

        st.session_state["messages"] = result_state.get("messages", st.session_state["messages"])

        if "error" in result_state:
            st.session_state["resultado"] = ""
            st.error(f"❌ Erro: {result_state['error']}")
        else:
            st.session_state["resultado"] = result_state.get("mensagem") or f"✅ Resultado: {result_state.get('result')}"

    for msg in st.session_state["messages"]:
        role = "Você" if getattr(msg, "role", None) == "user" else "Agente"
        content = getattr(msg, "content", str(msg))
        st.markdown(f"**{role}**: {content}")

    if st.session_state["resultado"]:
        st.markdown(f"### {st.session_state['resultado']}")

if __name__ == "__main__":
    main()
