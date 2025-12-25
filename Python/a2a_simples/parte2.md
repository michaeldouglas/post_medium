# A2A – Projeto Simples de Multi-Agentes

Primeiro instalar: uv add langchain langchain-ollama langgraph langgraph-cli[inmem] pydantic python-dotenv

Criar a pasta agent e depois, langchain com os scripts

## Execução de testes

python -m agents.balance.agent.langchain.tests.test_gpt_oss_com_tools
python -m agents.balance.agent.langchain.tests.test_gpt_oss_sem_tools

## Executando os evals

python -m agents.balance.agent.langchain.evals.datasets.balance_agent
python -m agents.balance.agent.langchain.evals.run_evals
