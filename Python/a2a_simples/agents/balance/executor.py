import logging
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from agent.langchain.saldo import run_balance_agent


logger = logging.getLogger("a2a")


class BalanceAgentExecutor(AgentExecutor):

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        logger.info("agent.execute.balance")

        # Obtem a mensagem
        user_text = context.get_user_input()

        # Executa o agente de saldo
        response_balance_agent = run_balance_agent(user_text)

        await event_queue.enqueue_event(
            new_agent_text_message(response_balance_agent)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        logger.info("agent.cancel.balance")
