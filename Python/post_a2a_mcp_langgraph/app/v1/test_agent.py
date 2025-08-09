from agents import graph
from langchain_core.messages import AIMessage

def extrair_resposta_final(mensagens, operacao):
    ordem = ["multiplicar", "somar", "subtrair"]

    if operacao not in ordem:
        return "Operação inválida"

    index = ordem.index(operacao)

    respostas = [
        m.content for m in mensagens
        if isinstance(m, AIMessage) and m.content and "Transferring back" not in m.content
    ]

    if len(respostas) > index:
        return respostas[index]
    else:
        return "Resultado não encontrado"

def main():
    print("Calculadora básica usando LangGraph")
    print("Operações disponíveis: somar, subtrair, multiplicar")

    operacao = input("Digite a operação: ").strip().lower()
    try:
        a = int(input("Digite o primeiro número: ").strip())
        b = int(input("Digite o segundo número: ").strip())
    except ValueError:
        print("Por favor, digite números inteiros válidos.")
        return

    try:
        resultado = graph.invoke({
            "operacao": operacao,
            "dados": (a, b)
        })

        res = resultado.get("resultado")
        print("Resultado:", extrair_resposta_final(res, operacao))

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
