from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from ..tools import consultar_saldo


def main():
    llm = init_chat_model(
        model="gpt-oss",
        model_provider="ollama",
        temperature=0,
    )

    print("Iniciando teste do modelo gpt-oss...\n")

    tools = [consultar_saldo]

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=(
            "Você é um agente de consulta de saldos. "
            "Quando o cliente perguntar sobre saldo, "
            "utilize a ferramenta `consultar_saldo`."
        ),
    )

    print("Chamando o agente...\n")

    result = agent.invoke({
        "messages": [
            HumanMessage(content="Qual é o saldo do cliente João Silva?")
        ]
    })

    print("\n======================== Resposta final ========================\n")
    for message in result["messages"]:
        message.pretty_print()
        print()


if __name__ == "__main__":
    main()
