from schema.calc_state import CalcState
from call_tool import call_mcp_tool

async def subtrair(state: CalcState) -> CalcState:
    resultado = await call_mcp_tool("subtrair", state["num1"], state["num2"])
    return {**state, "result": resultado}