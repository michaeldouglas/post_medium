import uuid
import httpx
import asyncio
from typing import Optional

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import (
    AgentCard,
    Message,
    Part,
    Role,
    TextPart,
)

# AGENTES DISPONÍVEIS
AGENTS = {
    "oi": "http://localhost:8080",
    "tchau": "http://localhost:8081",
}

TIMEOUT = 5  # segundos


async def call_agent_safe(name: str, base_url: str, text: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as httpx_client:
            print(f"Conectando ao agente '{name}' em {base_url}")

            # Resolve o Agent Card
            resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=base_url,
            )

            agent_card: AgentCard = await resolver.get_agent_card()

            # CONFIG OFICIAL (CONFORME DOCUMENTAÇÃO)
            config = ClientConfig(
                httpx_client=httpx_client,
                streaming=False,  # igual ao exemplo da doc
            )

            # FACTORY + CLIENT REAL
            factory = ClientFactory(config)
            client = factory.create(agent_card)

            # MENSAGEM NO PADRÃO NOVO
            message = Message(
                role=Role.user,
                message_id=str(uuid.uuid4()),
                parts=[Part(root=TextPart(text=text))],
            )

            # SEND_MESSAGE RETORNA UM ASYNC ITERATOR
            async for event in client.send_message(message):
                # O evento final normalmente é um Message
                if isinstance(event, Message):
                    for part in event.parts:
                        if part.root.kind == "text":
                            return part.root.text

            return None

    except httpx.ConnectError:
        print(f"Agente '{name}' fora do ar.")
        return None

    except asyncio.TimeoutError:
        print(f"Timeout no agente '{name}'.")
        return None

    except Exception as e:
        print(f"Erro no agente '{name}': {str(e)}")
        return None


async def main():
    print("\nIniciando orquestração resiliente...\n")

    for name, url in AGENTS.items():
        resposta = await call_agent_safe(name, url, name)

        if resposta:
            print(f"Resposta do agente '{name}': {resposta}\n")
        else:
            print(f"Pulando agente '{name}' e continuando...\n")

    print("Orquestração finalizada com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
