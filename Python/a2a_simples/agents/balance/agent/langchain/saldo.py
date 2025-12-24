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


_llm = init_chat_model(
    model="gpt-oss",
    model_provider="ollama",
    base_url="http://host.docker.internal:11434",
    temperature=0,
)

_agent = create_agent(
    _llm,
    tools=[consultar_saldo],
    system_prompt=(
        "Você é um agente de consulta de saldos. "
        "Quando o cliente perguntar sobre saldo, "
        "utilize a ferramenta `consultar_saldo`."
    ),
)


def run_balance_agent(user_text: str) -> str:
    """
    Recebe o texto do usuário e devolve apenas a resposta.
    """
    result = _agent.invoke({
        "messages": [
            HumanMessage(content=user_text)
        ]
    })

    return result["messages"][-1].content
