import uuid
import httpx
import asyncio
import random
from typing import Optional

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import AgentCard, Message, Part, Role, TextPart

# AGENTES DISPONÍVEIS
AGENTS = {
    "cartao": "http://localhost:8081",
    "saldo": "http://localhost:8082",
}

# CONFIG AVANÇADA
BASE_TIMEOUT = 3          # timeout base
MAX_RETRIES = 3           # tentativas por agente
BACKOFF_BASE = 0.8        # fator de backoff


async def call_agent_safe(name: str, base_url: str, text: str) -> Optional[str]:
    """
    Chamada segura de agente com:
    - timeout inteligente
    - retry com backoff
    - ClientFactory oficial
    - streaming async real
    """

    for attempt in range(1, MAX_RETRIES + 1):
        timeout = BASE_TIMEOUT + attempt  # timeout progressivo

        try:
            async with httpx.AsyncClient(timeout=timeout) as httpx_client:
                print(f"[{name}] tentativa {attempt} | timeout={timeout}s")

                # Resolve o Agent Card
                resolver = A2ACardResolver(
                    httpx_client=httpx_client,
                    base_url=base_url,
                )

                agent_card: AgentCard = await resolver.get_agent_card()

                # CONFIG OFICIAL
                config = ClientConfig(
                    httpx_client=httpx_client,
                    streaming=False,
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

                # STREAMING ASSÍNCRONO REAL
                async for event in client.send_message(message):
                    if isinstance(event, Message):
                        for part in event.parts:
                            if part.root.kind == "text":
                                print(f"[{name}] resposta recebida")
                                return part.root.text

                raise RuntimeError("Resposta vazia do agente")

        except (httpx.TimeoutException, asyncio.TimeoutError):
            print(f"[{name}] timeout na tentativa {attempt}")

        except httpx.ConnectError:
            print(f"[{name}] agente fora do ar")

        except Exception as e:
            print(f"[{name}] erro: {str(e)}")

        # BACKOFF EXPONENCIAL COM JITTER
        if attempt < MAX_RETRIES:
            delay = BACKOFF_BASE * (2 ** (attempt - 1)) + \
                random.uniform(0, 0.3)
            print(f"[{name}] retry em {delay:.2f}s...\n")
            await asyncio.sleep(delay)

    print(f"[{name}] falhou após {MAX_RETRIES} tentativas\n")
    return None


async def main():
    print("\n Orquestração PARALELA iniciada...\n")

    tasks = [
        call_agent_safe(name, url, name)
        for name, url in AGENTS.items()
    ]

    # EXECUÇÃO PARALELA REAL
    results = await asyncio.gather(*tasks)

    print("\nRESULTADOS FINAIS:\n")

    for (name, _), resposta in zip(AGENTS.items(), results):
        if resposta:
            print(f"{name}: {resposta}")
        else:
            print(f"{name}: falhou")

    print("\nOrquestração paralela finalizada com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
