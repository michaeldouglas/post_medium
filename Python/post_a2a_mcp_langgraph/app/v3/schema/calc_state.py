from typing import TypedDict, Literal

class CalcState(TypedDict):
    num1: int
    num2: int
    operation: Literal["somar", "subtrair", "multiplicar"]
    result: int | float | None
    mensagem: str | None