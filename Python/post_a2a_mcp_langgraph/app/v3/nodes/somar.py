from schema.calc_state import CalcState
from call_tool import call_mcp_tool

async def somar(state: CalcState) -> CalcState:
    resultado = await call_mcp_tool("somar", state["num1"], state["num2"])
    return {**state, "result": resultado}