def tool_usage_evaluator(run, example):
    expected_tool = example.outputs.get("expected_tool")
    used_tools = run.outputs.get("tools_used", [])

    if expected_tool is None:
        return {
            "key": "tool_usage",
            "score": 1.0,
            "commentary": "Nenhuma ferramenta esperada"
        }

    return {
        "key": "tool_usage",
        "score": 1.0 if expected_tool in used_tools else 0.0,
        "commentary": f"Esperado: {expected_tool}, usado: {used_tools}"
    }
