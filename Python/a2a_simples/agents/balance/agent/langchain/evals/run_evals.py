from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate

from .targets.balance_agent import balance_agent_target
from .evaluators.tool_usage import tool_usage_evaluator
from .evaluators.intent import intent_evaluator

load_dotenv()
client = Client()

if __name__ == "__main__":
    evaluate(
        balance_agent_target,
        data="a2a-balance-agent-eval",
        evaluators=[
            tool_usage_evaluator,
            intent_evaluator,
        ],
        experiment_prefix="a2a-balance-agent-evals",
        client=client,
    )

    print("Evals finalizados")
