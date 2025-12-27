import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from .tools import consultar_saldo
import langsmith as ls

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-oss")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
PROJECT_NAME = os.getenv("LANGSMITH_PROJECT", "a2a-agents")

EVAL_MODE = os.getenv("EVAL_MODE", "false").lower() == "true"

if EVAL_MODE:
    BASE_URL = "http://localhost:11434"
else:
    BASE_URL = os.getenv(
        "BASE_URL",
        "http://host.docker.internal:11434"
    )

_llm = init_chat_model(
    model=MODEL,
    model_provider=MODEL_PROVIDER,
    base_url=BASE_URL,
    temperature=TEMPERATURE,
)

_agent = create_agent(
    _llm,
    tools=[consultar_saldo],
    system_prompt=(
        "Você é um agente de consulta de saldos. "
        "Quando o cliente perguntar sobre saldo, "
        "utilize a ferramenta `consultar_saldo`."
    )
)


def run_balance_agent(user_text: str, request_id: str | None) -> str:
    metadata = {
        "agent_name": "balance-agent",
        "workflow": "a2a",
        "service": "a2a-agents",
        "env": os.getenv("ENV", "dev"),
        "request_id": request_id
    }

    with ls.tracing_context(
        project_name=PROJECT_NAME,
        enabled=True,
        metadata=metadata
    ):
        result = _agent.invoke({
            "messages": [
                HumanMessage(content=user_text)
            ]
        })

        print(f"[balance-agent][{request_id}] input={user_text}")
        print(
            f"[balance-agent][{request_id}] output={result['messages'][-1].content}")

        return result["messages"][-1].content
