"""Run MCP Gateway with example tools."""
from datetime import datetime
from dotenv import load_dotenv
import re
import os
import sys
import io
from fastmcp import FastMCP
import httpx

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

mcp = FastMCP("FinHub")

@mcp.tool
async def analise_acao(texto: str = "PETR4"):
    """
    Retorna um resumo formatado de uma ação (ex: PETR4, VALE3) com base na API brapi.dev.
    O nome do ativo pode ser extraído automaticamente do texto enviado.
    Exemplo de uso:
    - "Retorne um resumo formatado da ação PETR4"
    - "Analise VALE3 no último mês"
    """
    try:
        match = re.search(r"\b([A-Z]{4}\d)\b", texto.upper())
        ativo = match.group(1) if match else texto.upper().strip()

        hoje = datetime.today()
        BRAPI_KEY = os.getenv("BRAPI_KEY")
        url = f"https://brapi.dev/api/quote/{ativo}.SA?range=1mo&interval=1d&token={BRAPI_KEY}"

        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        results = data.get("results", [])
        if not results:
            return f"Não foi possível obter dados da ação {ativo}."

        acao = results[0]

        if "historicalData" in acao and acao["historicalData"]:
            historico = acao["historicalData"]
            fechamento_inicial = historico[0]["close"]
            fechamento_final = historico[-1]["close"]
            maximo = max(day["high"] for day in historico)
            minimo = min(day["low"] for day in historico)
            variacao = fechamento_final - fechamento_inicial
            percentual = (variacao / fechamento_inicial) * 100
            direcao = "alta" if variacao > 0 else "queda"

            return (
                f"**Desempenho da {ativo} no último mês**\n"
                f"- Preço inicial: R$ {fechamento_inicial:.2f}\n"
                f"- Preço final: R$ {fechamento_final:.2f}\n"
                f"- Variação: R$ {variacao:.2f} ({percentual:.2f}%) → {direcao}\n"
                f"- Máximo do período: R$ {maximo:.2f}\n"
                f"- Mínimo do período: R$ {minimo:.2f}\n"
                f"- Data da análise: {hoje.strftime('%d/%m/%Y')}\n"
            )

        preco_atual = acao.get("regularMarketPrice", 0)
        variacao = acao.get("regularMarketChange", 0)
        variacao_pct = acao.get("regularMarketChangePercent", 0)
        abertura = acao.get("regularMarketOpen", 0)
        fechamento_anterior = acao.get("regularMarketPreviousClose", 0)
        faixa_52w = acao.get("fiftyTwoWeekRange", "0 - 0")

        try:
            min_52w, max_52w = [
                float(x.strip()) if x.strip().replace('.', '', 1).isdigit() else 0.0
                for x in faixa_52w.split('-')
            ]
        except Exception:
            min_52w, max_52w = 0.0, 0.0

        direcao = "alta" if variacao > 0 else "queda"

        return (
            f"**Resumo de {ativo}**\n"
            f"- Preço atual: R$ {preco_atual:.2f}\n"
            f"- Variação diária: {variacao:.2f} ({variacao_pct:.2f}%) → {direcao}\n"
            f"- Abertura: R$ {abertura:.2f}\n"
            f"- Fechamento anterior: R$ {fechamento_anterior:.2f}\n"
            f"- Faixa de 52 semanas: R$ {min_52w:.2f} - R$ {max_52w:.2f}\n"
            f"- Data da análise: {hoje.strftime('%d/%m/%Y')}\n"
        )

    except Exception as e:
        return f"Ocorreu um erro ao consultar {ativo}: {str(e)}"

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8081,
        stateless_http=False, # False ele fica stateful (mantém sessão), True ele fica stateless (nova sessão a cada requisição)
        path="/mcp_gateway"
    )
