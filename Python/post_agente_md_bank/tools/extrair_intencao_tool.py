from langchain.tools import tool
import re


@tool("extrair_intencao", return_direct=False)
def extrair_intencao_tool(texto: str) -> str:
    """Detecta a intenção principal do texto do usuário (ex: cartão de crédito, conta corrente, etc)."""
    texto = texto.lower()

    padroes = {
        "cartao_de_credito": r"(cart[aã]o|credito|crédito)",
        "conta_corrente": r"(conta\s*corrente|minha\s*conta)",
        "emprestimo": r"(emprestimo|empr[eé]stimo|pegar\s*dinheiro)",
        "investimentos": r"(investir|investimento|aplica[cç][aã]o)"
    }

    for nome, regex in padroes.items():
        if re.search(regex, texto):
            return nome
    return "outro"
