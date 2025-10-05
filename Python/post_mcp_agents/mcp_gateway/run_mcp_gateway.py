from fastmcp import FastMCP
from datetime import datetime
import httpx

mcp = FastMCP("Demo 🚀")

@mcp.tool
def soma(a: int, b: int) -> int:
    """Soma dois números"""
    total = a + b
    return f"O resultado é: {total}"

@mcp.tool
def subtracao(a: int, b: int) -> int:
    """Subtrai b de a"""
    return a - b

@mcp.tool
async def analise_petr4_ultimo_mes():
    """
    Realiza a avaliação de uma ação
    """
    try:
        # Define período do último mês
        hoje = datetime.today()
        url = "https://brapi.dev/api/quote/PETR4.SA?range=1mo&token=mRVB9Cgc1k5DwcXdzaP8kd"

        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        results = data.get("results", [])
        if not results or not results[0].get("historicalData"):
            return "Não foi possível obter dados históricos da PETR4 no último mês."

        historico = results[0]["historicalData"]

        fechamento_inicial = historico[0]["close"]
        fechamento_final = historico[-1]["close"]
        maximo = max(day["high"] for day in historico)
        minimo = min(day["low"] for day in historico)

        variacao = fechamento_final - fechamento_inicial
        percentual = (variacao / fechamento_inicial) * 100

        resposta = (
            f"Desempenho da PETR4 no último mês:\n"
            f"- Preço inicial: {fechamento_inicial:.2f} BRL\n"
            f"- Preço final: {fechamento_final:.2f} BRL\n"
            f"- Variação: {variacao:.2f} BRL ({percentual:.2f}%)\n"
            f"- Máximo do período: {maximo:.2f} BRL\n"
            f"- Mínimo do período: {minimo:.2f} BRL\n"
            f"- Dia solicitado: {hoje}\n"
        )

        return resposta

    except Exception as e:
        return f"Ocorreu um erro ao consultar a PETR4: {str(e)}"

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8081,
        path="/mcp_gateway"
    )
