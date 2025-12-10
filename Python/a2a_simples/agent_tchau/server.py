import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from executor import TchauAgentExecutor


def main():
    skill = AgentSkill(
        id="tchau",
        name="Dizer Tchau",
        description="Retorna um Tchau",
        tags=["tchau"],
        examples=["tchau"],
    )

    agent_card = AgentCard(
        name="Agente TCHAU",
        description="Agente que responde Tchau",
        url="http://localhost:8081/",
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[skill],
        version="1.0.0",
        capabilities=AgentCapabilities(),
    )

    handler = DefaultRequestHandler(
        agent_executor=TchauAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        http_handler=handler,
        agent_card=agent_card,
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=8081)


if __name__ == "__main__":
    main()
