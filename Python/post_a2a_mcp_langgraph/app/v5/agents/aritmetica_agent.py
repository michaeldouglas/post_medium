import os
import json
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schema import CalcState

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))


async def aritmetica_node(state: CalcState):
    system_message = {
        "role": "system",
        "content": (
            "Você é um agente decisor de aritmética que entende pedidos de contas simples: somar, subtrair e multiplicar. "
            "O usuário pode escrever o pedido de formas variadas, por exemplo: "
            "'some 5 e 5', 'por favor subtraia 10 menos 3', 'multiplicar 4 por 6', 'quanto é 2 + 2?', '5 vezes 7', etc. "
            "Sua tarefa é identificar qual operação o usuário deseja fazer e extrair dois números (inteiros ou decimais). "
            "Você só sabe realizar três operações: 'somar', 'subtrair' e 'multiplicar'. "
            "Responda SEMPRE APENAS com um JSON com exatamente três campos: "
            "\"operation\": uma das strings \"somar\", \"subtrair\", \"multiplicar\", "
            "\"num1\": primeiro número, "
            "\"num2\": segundo número. "
            "Exemplo de resposta válida: {\"operation\": \"somar\", \"num1\": 5, \"num2\": 5}. "
            "Se o pedido do usuário não corresponder a nenhuma das operações que você suporta, responda: "
            "{\"operation\": \"desconhecido\", \"num1\": 0, \"num2\": 0}. "
            "Não escreva nada além do JSON, nem explicações, nem comentários."
        )
    }

    messages = [system_message] + state["messages"]

    response = await llm.ainvoke(messages)
    resposta_texto = response.content.strip()

    try:
        data = json.loads(resposta_texto)
        operacao = data.get("operation", "desconhecido")
        num1 = data.get("num1", 0)
        num2 = data.get("num2", 0)
    except json.JSONDecodeError:
        operacao = "desconhecido"
        num1, num2 = 0, 0

        texto_lower = resposta_texto.lower()
        if "somar" in texto_lower:
            operacao = "somar"
        elif "subtrair" in texto_lower:
            operacao = "subtrair"
        elif "multiplicar" in texto_lower:
            operacao = "multiplicar"

        nums = re.findall(r"[-+]?\d*\.\d+|\d+", resposta_texto)
        if len(nums) >= 2:
            num1, num2 = float(nums[0]), float(nums[1])

    return {
        **state,
        "operation": operacao,
        "num1": num1,
        "num2": num2,
        "messages": state["messages"] + [response],
    }
