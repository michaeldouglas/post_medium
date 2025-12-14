import logging
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message

logger = logging.getLogger("a2a")


class BalanceAgentExecutor(AgentExecutor):

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        logger.info("agent.execute.balance")

        await event_queue.enqueue_event(
            new_agent_text_message("Seu saldo atual é de R$ 1.500,00.")
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        logger.info("agent.cancel.balance")
