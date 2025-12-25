from langchain.tools import tool

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
