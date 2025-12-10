# A2A - Projeto Simples de Multi Agentes

## Descrição

O projeto **A2A Simples** é uma aplicação simples que demonstra a execução de agentes, envio e recebimento de mensagens, e gerenciamento de eventos. Possui um agente para dar oi e outro para dar tchau.

## Funcionalidades

- Execução de agentes de forma assíncrona.
- Envio e recebimento de mensagens.
- Gerenciamento de eventos via fila.
- Estrutura modular para fácil manutenção.

## Estrutura do Projeto

```
a2a/
├── agent_oi/         # Agente simples para oi
├── agent_tchau/      # Agente simples para tchau
├── client/           # Execução da orquestração
└── README.md         # Este arquivo
```

## Instalação

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd a2a
```

2. Instale as dependências:

```bash
uv sync
```

## Uso

1. Forma simples:

```bash
python .\client\test_client.py
```

2. Segunda forma:

```python
python .\client\test_client2.py
```

## Contribuição

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
