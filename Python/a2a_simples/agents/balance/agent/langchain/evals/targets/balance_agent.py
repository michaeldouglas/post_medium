from ...saldo import run_balance_agent


def balance_agent_target(example: dict) -> dict:
    user_input = example["input"]

    output = run_balance_agent(user_input, None)

    return {
        "output": output,
        "tools_used": []
    }
