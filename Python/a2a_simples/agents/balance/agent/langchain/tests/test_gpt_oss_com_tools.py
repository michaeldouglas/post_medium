from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import create_agent

CLIENTES = {
    "joão silva": {
        "id": 1,
        "nome": "João Silva",
        "saldo": 1500.75,
    },
    "maria oliveira": {
        "id": 2,
        "nome": "Maria Oliveira",
        "saldo": 2450.00,
    },
    "carlos pereira": {
        "id": 3,
        "nome": "Carlos Pereira",
        "saldo": 320.40,
    },
}


@tool
def consultar_saldo(nome_cliente: str) -> str:
    """Encontra o cliente pelo nome e retorna o saldo."""
    key = nome_cliente.lower().strip()
    cliente = CLIENTES.get(key)
    if not cliente:
        return f"Cliente '{nome_cliente}' não encontrado."
    return f"O saldo do cliente {cliente['nome']} é R$ {cliente['saldo']:.2f}"


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
