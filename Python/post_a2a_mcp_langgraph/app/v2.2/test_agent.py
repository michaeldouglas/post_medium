import argparse
from agents import graph

def run_graph(num1: int, num2: int, operation: str):
    estado_inicial = {
        "num1": num1,
        "num2": num2,
        "operation": operation,
        "result": None,
    }
    resultado = graph.invoke(estado_inicial)
    print(f"Resultado: {resultado['result']}")

def interactive_mode():
    print("Modo interativo da calculadora. Digite 'sair' para encerrar.")
    while True:
        op = input("Operação (somar, subtrair, multiplicar): ").strip().lower()
        if op == "sair":
            break
        if op not in ("somar", "subtrair", "multiplicar"):
            print("Operação inválida! Tente novamente.")
            continue
        
        try:
            n1 = input("Número 1: ").strip()
            if n1.lower() == "sair":
                break
            n1 = int(n1)

            n2 = input("Número 2: ").strip()
            if n2.lower() == "sair":
                break
            n2 = int(n2)
        except ValueError:
            print("Por favor, digite um número válido.")
            continue
        
        run_graph(n1, n2, op)
        print("---")

def main():
    parser = argparse.ArgumentParser(description="Calculadora LangGraph CLI")
    parser.add_argument("num1", nargs="?", type=int, help="Primeiro número")
    parser.add_argument("num2", nargs="?", type=int, help="Segundo número")
    parser.add_argument(
        "operation",
        nargs="?",
        choices=["somar", "subtrair", "multiplicar"],
        help="Operação a ser realizada",
    )
    args = parser.parse_args()

    if args.num1 is not None and args.num2 is not None and args.operation is not None:
        run_graph(args.num1, args.num2, args.operation)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
