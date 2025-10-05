import os
import re
import time
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from fastmcp import Client
from src.schemas.chat import ChatRequest
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
logger = logging.getLogger("uvicorn")

model = ChatOpenAI(
    model="gpt-4-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

mcp_llm_client = MultiServerMCPClient({
    "mcpstore": {
        "url": "http://localhost:8081/mcp_gateway",
        "transport": "streamable_http"
    }
})

mcp_client = Client("http://localhost:8081/mcp_gateway")
preloaded_tools = None


async def preload_tools():
    start_time = time.time()
    tools = await mcp_llm_client.get_tools()
    elapsed = time.time() - start_time
    logger.info(f"[INIT] Tempo para pré-carregar tools: {elapsed:.3f}s")
    return tools


async def get_agent():
    global preloaded_tools
    if preloaded_tools is None:
        preloaded_tools = await preload_tools()
    prompt_base = (
        "Você é um agente especializado em mercado financeiro. "
        "Forneça informações sobre ações, cotações, históricos, dividendos e fundamentos. "
        "Responda apenas perguntas relacionadas a investimentos e mercado de capitais, "
        "e recuse-se a outros assuntos. "
        "Crie respostas curtas e objetivas, simples para o usuário leigo entender."
    )
    agent = create_react_agent(
        model=model,
        tools=preloaded_tools,
        prompt=prompt_base
    )
    return agent


@router.post(
    "/chat",
    tags=["Chat"],
    summary="Enviar mensagem para o agente financeiro",
    response_description="Resposta do agente LLM financeiro"
)
async def chat_endpoint(payload: ChatRequest):
    """
    Recebe um JSON com a mensagem do usuário e retorna uma resposta gerada pelo agente financeiro (LLM).

    ### Request Example:
    ```json
    {
        "user": "Michael",
        "message": "Qual o resumo da PETR4?"
    }
    ```

    ### Response Example:
    ```json
    {
        "reply": "PETR4 está cotada em R$ 31, com variação de -0,26% hoje..."
    }
    ```
    """
    start_total = time.time()
    texto = payload.message
    logger.info(f"[CHAT] Prompt recebido: {texto}")

    try:
        start_tools = time.time()
        agent = await get_agent()
        elapsed_tools = time.time() - start_tools
        logger.info(f"[CHAT] Tempo para obter agent: {elapsed_tools:.3f}s")

        start_exec = time.time()
        response = await agent.ainvoke({"messages": texto})
        elapsed_exec = time.time() - start_exec
        logger.info(f"[CHAT] Tempo de execução do agente: {elapsed_exec:.3f}s")

        reply = response["messages"][-1].content
        elapsed_total = time.time() - start_total
        logger.info(f"[CHAT] Tempo total do endpoint: {elapsed_total:.3f}s")

        return JSONResponse(content={"reply": reply})

    except Exception as e:
        logger.error(f"[CHAT] Erro LLM financeiro: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post(
    "/acao",
    tags=["Ação"],
    summary="Obter resumo de uma ação",
    response_description="Resumo da ação via tool MCP direta"
)
async def acao_endpoint(payload: ChatRequest):
    """
    Recebe um JSON com a mensagem do usuário contendo um ticker de ação e retorna um resumo via tool MCP.

    ### Request Example:
    ```json
    {
        "user": "Michael",
        "message": "Retorne um resumo formatado da ação PETR4"
    }
    ```

    ### Response Example:
    ```json
    {
        "reply": "📊 Resumo de PETR4 (Petrobras PN)..."
    }
    ```
    """
    start_total = time.time()
    texto = payload.message.upper()
    logger.info(f"[AÇÃO] Texto recebido: {texto}")

    match = re.search(r"\b([A-Z]{4}\d)\b", texto)
    if not match:
        return JSONResponse(content={"error": "Nenhum ticker válido encontrado no texto."}, status_code=400)

    ativo = match.group(1)

    try:
        start_mcp = time.time()
        async with mcp_client:
            result = await mcp_client.call_tool("analise_acao", {"texto": ativo})
        elapsed_mcp = time.time() - start_mcp
        logger.info(f"[AÇÃO] Tempo execução tool MCP: {elapsed_mcp:.3f}s")

        if result.content and len(result.content) > 0 and hasattr(result.content[0], "text"):
            resposta = result.content[0].text
        else:
            resposta = "Sem resposta da tool."

        elapsed_total = time.time() - start_total
        logger.info(f"[AÇÃO] Tempo total do endpoint: {elapsed_total:.3f}s")

        return JSONResponse(content={"reply": resposta})

    except Exception as e:
        logger.error(f"[AÇÃO] Erro MCP Gateway: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
