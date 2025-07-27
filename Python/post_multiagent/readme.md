# MDBank

<img src="image.jpeg" width="280" height="250" alt="MDBank Supervisor Agents" />

Projeto de estudos sobre agentes autônomos utilizando Python e Docker Compose, utilizando o framework FastAPI. O projeto simula um sistema bancário com três agentes: um agente de supervisão, um agente de consulta de saldo e um agente de consulta de cartão de crédito.

A ideia é demonstrar o design pattern de agentes autônomos usando Supervisor, onde cada agente é responsável por uma tarefa específica e se comunica com os outros agentes para completar uma transação bancária.

## Subir o projeto

Para subir o projeto, execute o seguinte comando no terminal:

```bash
docker-compose up --build -d
```

Exemplo de curl

```bash
curl --request POST \
  --url http://localhost:8080/chat \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.1' \
  --data '{
    "message": "Qual é o limite do cartão de crédito?",
	  "client_id": "cliente123",
	  "session_id": "123123123231"
}'
```

O projeto responde em três endpoints:

- **[/chat](http://localhost:8080/chat)**: Endpoint principal que recebe a mensagem do cliente e inicia o processo de consulta.
- **[/saldo](http://localhost:8082/saldo)**: Endpoint do agente de consulta de saldo, que retorna o saldo bancário do cliente.
- **[/cartao](http://localhost:8081/cartao)**: Endpoint do agente de consulta de cartão de crédito, que retorna o limite do cartão de crédito do cliente.