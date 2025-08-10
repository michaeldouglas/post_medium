from typing import TypedDict, Literal
from typing import Annotated
from langgraph.graph.message import add_messages

class CalcState(TypedDict):
    num1: int
    num2: int
    operation: Literal["somar", "subtrair", "multiplicar"]
    result: int | float | None
    mensagem: str | None
    started_at: str | None
    finished_at: str | None
    messages: Annotated[list, add_messages]