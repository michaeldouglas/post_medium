from schema.calc_state import CalcState
from call_tool import call_mcp_tool

async def multiplicar(state: CalcState) -> CalcState:
    resultado = await call_mcp_tool("multiplicar", state["num1"], state["num2"])
    return {**state, "result": resultado}