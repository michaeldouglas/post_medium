from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from executor import CardAgentExecutor

skill = AgentSkill(
    id="cartao_credito",
    name="Consulta de Cartão de Crédito",
    description="Fornece informações sobre cartão de crédito, como limite, fatura e vencimento.",
    tags=["cartao", "credito", "fatura", "limite"],
    examples=[
        "qual o limite do meu cartão?",
        "quando vence minha fatura?",
        "qual o valor da fatura atual?"
    ],
)

agent_card = AgentCard(
    name="Agente de Cartão de Crédito",
    description="Agente responsável por responder perguntas sobre cartão de crédito.",
    url="http://localhost:8081/",
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[skill],
    version="1.0.0",
    capabilities=AgentCapabilities(),
)

handler = DefaultRequestHandler(
    agent_executor=CardAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    http_handler=handler,
    agent_card=agent_card,
)

app = server.build()
