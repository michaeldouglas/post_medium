from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message


class CardAgentExecutor(AgentExecutor):

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        await event_queue.enqueue_event(
            new_agent_text_message("O saldo do seu cartão é R$ 1.234,56.")
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        pass
