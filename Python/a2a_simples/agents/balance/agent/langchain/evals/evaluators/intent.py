def normalize_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            part["text"] if isinstance(
                part, dict) and "text" in part else str(part)
            for part in content
        )
    return str(content)


def intent_evaluator(run, example):
    expected_intent = example.outputs.get("expected_intent")
    agent_output = run.outputs.get("output")

    if not expected_intent or not agent_output:
        return {
            "key": "intent_match",
            "score": 0.0,
            "commentary": "Output ou intent ausente"
        }

    ok = expected_intent.lower() in agent_output.lower()

    return {
        "key": "intent_match",
        "score": 1.0 if ok else 0.0,
        "commentary": f"Esperado: {expected_intent}"
    }
