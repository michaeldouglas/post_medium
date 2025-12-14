from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from executor import TchauAgentExecutor

# -----------------------
# Definição do skill
# -----------------------
skill = AgentSkill(
    id="saldo",
    name="Consulta de Saldo",
    description="Informa o saldo disponível e movimentações recentes da conta.",
    tags=["saldo", "conta", "extrato"],
    examples=[
        "qual é o meu saldo?",
        "quanto dinheiro eu tenho na conta?",
        "mostrar extrato recente"
    ],
)

# -----------------------
# Agent Card
# -----------------------
agent_card = AgentCard(
    name="Agente de Saldo",
    description="Agente responsável por informar saldo e extrato da conta.",
    url="http://localhost:8081/",
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[skill],
    version="1.0.0",
    capabilities=AgentCapabilities(),
)

# -----------------------
# Request Handler
# -----------------------
handler = DefaultRequestHandler(
    agent_executor=TchauAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

# -----------------------
# A2A Application
# -----------------------
server = A2AStarletteApplication(
    http_handler=handler,
    agent_card=agent_card,
)

# EXPOSIÇÃO DO APP PARA O UVICORN
app = server.build()
