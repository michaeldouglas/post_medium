from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.chat_models import init_chat_model
from tools.extrair_intencao_tool import extrair_intencao_tool
from schema.faq_state import FaqState
import os
import json
from dotenv import load_dotenv

# Carrega API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY
)
model_with_tools = model.bind_tools([extrair_intencao_tool])
tools_by_name = {extrair_intencao_tool.name: extrair_intencao_tool}


def receber_mensagem(state: FaqState) -> FaqState:
    """Node que envia mensagens para LLM e atualiza intenção."""

    # Se não houver histórico, cria a mensagem do usuário
    if not state.messages:
        state.messages = [HumanMessage(
            content="Usuário: " + state.resposta or "")]

    # Invoca LLM
    response = model_with_tools.invoke(
        [SystemMessage(
            content="Você é um assistente de atendimento ao cliente.")] + state.messages
    )

    # Adiciona ao histórico
    state.messages.append(response)

    # Se LLM chamou tool, executa e adiciona ToolMessage
    for tool_call in getattr(response, "tool_calls", []):
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        state.messages.append(ToolMessage(
            content=observation, tool_call_id=tool_call["id"]))

        # Atualiza intenção do cliente a partir do resultado da tool
        state.intencao = observation

    # Também tenta extrair nome do cliente via JSON do LLM
    try:
        dados = json.loads(response.content)
        state.nome_cliente = dados.get("nome")
    except Exception:
        state.nome_cliente = None

    return state
