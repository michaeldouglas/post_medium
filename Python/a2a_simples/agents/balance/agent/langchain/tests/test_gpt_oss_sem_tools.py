from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
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


def main():
    llm = init_chat_model(
        model="gpt-oss",
        model_provider="ollama",
        temperature=0,
    )

    print("Iniciando teste do modelo gpt-oss...\n")

    agent = create_agent(
        llm,
        system_prompt=(
            "Você é um agente de consulta de saldos. "
        ),
    )

    print("Chamando o agente...\n")

    result = agent.invoke({
        "messages": [
            HumanMessage(
                content=[
                    "Qual é o saldo do cliente João Silva?"
                    "O CPF dele é: 123.456.789-00"
                    "O ID do cliente é: 1"
                ])
        ]
    })

    print("\n======================== Resposta final ========================\n")
    for message in result["messages"]:
        message.pretty_print()
        print()


if __name__ == "__main__":
    main()
