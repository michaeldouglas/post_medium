# A2A – Projeto Simples de Multi-Agentes

O **A2A Simples** é um projeto educacional que demonstra, na prática, como construir e orquestrar **múltiplos agentes** utilizando o protocolo **A2A (Agent-to-Agent)**.

O foco do projeto é mostrar:

- Descoberta de agentes via _Agent Card_
- Comunicação entre agentes
- Orquestração paralela com tolerância a falhas
- Uso do client oficial A2A
- Execução local com Docker e Docker Compose

> **Importante:** este projeto **não expõe uma API REST tradicional**. A comunicação entre agentes acontece exclusivamente via **A2A Client SDK**.

---

## Agentes Disponíveis

Atualmente o projeto contém dois agentes independentes:

### Card Agent

Responsável por responder perguntas relacionadas a **cartão de crédito**, como:

- Limite disponível
- Valor da fatura
- Data de vencimento

### Balance Agent

Responsável por responder perguntas relacionadas a **saldo e extrato**, como:

- Saldo atual
- Movimentações recentes

---

## Funcionalidades

- Execução de agentes de forma **assíncrona e paralela**
- Orquestração resiliente com:
  - timeout progressivo
  - retry com backoff
  - isolamento de falhas por agente
- Descoberta automática de agentes via `agent-card.json`
- Estrutura modular e extensível
- Ambiente de desenvolvimento com Docker

---

## Estrutura do Projeto

```
.
├── agents/
│   ├── card/                # Agente de cartão de crédito
│   │   ├── server.py
│   │   ├── executor.py
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   └── balance/             # Agente de saldo
│       ├── server.py
│       ├── executor.py
│       ├── Dockerfile
│       └── pyproject.toml
│
├── client/                  # Orquestrador A2A
│   ├── test_client.py       # Execução simples
│   └── test_client2.py      # Execução paralela com retry/backoff
│
├── docker-compose.yml       # Orquestração dos agentes
├── .env                     # Variáveis de ambiente
└── README.md                # Este arquivo
```

---

## Executando com Docker

### Subir os agentes

```bash
docker compose up -d --build
```

### Ver status

```bash
docker ps
```

### Descobrir os agentes

```bash
curl http://localhost:8081/.well-known/agent-card.json
curl http://localhost:8082/.well-known/agent-card.json
```

---

## Executando o Client (Orquestração)

### Execução simples

```bash
python ./client/test_client.py
```

### Execução paralela com tolerância a falhas

```bash
python ./client/test_client2.py
```

Esse modo executa os agentes **em paralelo**, com:

- retry automático
- backoff exponencial
- isolamento de falhas

---

## Observações Importantes

- O único endpoint HTTP público é:

```
GET /.well-known/agent-card.json
```

---

## Logs

Após subir o container configurar o Loki como DataSource, para isso utilize a URL:

```bash
http://loki:3100
```

Na sequência você poderá acessar: http://localhost:3000 com o usuário e senha:

- admin
- admin

E então poderá ver os logs do saldo:

```json
{service="balance_agent", level="INFO"}
| json
| message=~"request.end"
| line_format "{{.timestamp}} | {{.message}} | request_id={{.request_id}} duration_ms={{.duration_ms}} status={{.status_code}}"
```

Para cartões:

```json
{service="card_agent", level="INFO"}
| json
| message=~"request.end"
| line_format "{{.timestamp}} | {{.message}} | request_id={{.request_id}} duration_ms={{.duration_ms}} status={{.status_code}}"
```

# Parte 2

Como executar os testes e Evals.

## Execução de testes

python -m agents.balance.agent.langchain.tests.test_gpt_oss_com_tools
python -m agents.balance.agent.langchain.tests.test_gpt_oss_sem_tools

## Executando os evals

python -m agents.balance.agent.langchain.evals.datasets.balance_agent
python -m agents.balance.agent.langchain.evals.run_evals

## Tecnologias Utilizadas

- Python 3.13
- A2A Protocol
- Starlette
- HTTPX
- AsyncIO
- Docker / Docker Compose
- Grafana
- Loki

---

## Licença

Este projeto está licenciado sob a **MIT License**.

---

## Próximos Passos (Ideias)

- Adicionar gateway REST → A2A
- Implementar streaming de mensagens
- Adicionar métricas e observabilidade
- Suporte a mais agentes
- Deploy em Kubernetes

---
