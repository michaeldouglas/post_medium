import os
from dotenv import load_dotenv
from langsmith import Client, wrappers
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT
from schema.faq_state import FaqState
from langchain.messages import HumanMessage
from graph.workflow import create_workflow  # seu workflow
from openai import OpenAI

# -----------------------------
# Configuração das chaves de API
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não definida no .env")

client = Client()
openai_client = wrappers.wrap_openai(OpenAI(api_key=OPENAI_API_KEY))

# -----------------------------
# Criação do dataset de avaliação
# -----------------------------
ID_DATASET = "faq-md-bank-eval-v2"
dataset = client.create_dataset(
    dataset_name=ID_DATASET,
    description="Exemplos para avaliar o agente de banco MD Bank",
)

examples = [
    # Cartão de crédito
    {"inputs": {"mensagem": "Oi, quero saber sobre meu cartão de crédito"},
     "outputs": {"intencao": "cartao_de_credito"}},
    {"inputs": {"mensagem": "Qual é o limite do meu cartão?"},
     "outputs": {"intencao": "cartao_de_credito"}},
    {"inputs": {"mensagem": "Como posso desbloquear meu cartão?"},
     "outputs": {"intencao": "cartao_de_credito"}},

    # Investimentos
    {"inputs": {"mensagem": "Como posso investir meu dinheiro?"},
     "outputs": {"intencao": "investimentos"}},
    {"inputs": {"mensagem": "Quais são as opções de fundos disponíveis?"},
     "outputs": {"intencao": "investimentos"}},
    {"inputs": {"mensagem": "Quero investir em ações"},
     "outputs": {"intencao": "investimentos"}},

    # Conta corrente
    {"inputs": {"mensagem": "Quero abrir uma conta corrente"},
     "outputs": {"intencao": "conta_corrente"}},
    {"inputs": {"mensagem": "Como faço para fechar minha conta?"},
     "outputs": {"intencao": "conta_corrente"}},
    {"inputs": {"mensagem": "Quais são as tarifas da conta corrente?"},
     "outputs": {"intencao": "conta_corrente"}},

    # Empréstimo
    {"inputs": {"mensagem": "Gostaria de pegar um empréstimo"},
     "outputs": {"intencao": "emprestimo"}},
    {"inputs": {"mensagem": "Qual é a taxa de juros do empréstimo pessoal?"},
     "outputs": {"intencao": "emprestimo"}},
    {"inputs": {"mensagem": "Como solicitar financiamento?"},
     "outputs": {"intencao": "emprestimo"}},

    # Outros / dúvidas gerais
    {"inputs": {"mensagem": "Algo que não entendi"},
     "outputs": {"intencao": "outro"}},
    {"inputs": {"mensagem": "Preciso de ajuda com algo"},
     "outputs": {"intencao": "outro"}},
    {"inputs": {"mensagem": "Não sei como usar o aplicativo"},
     "outputs": {"intencao": "outro"}},

    # Perguntas de saldo e extrato
    {"inputs": {"mensagem": "Qual é meu saldo atual?"},
     "outputs": {"intencao": "saldo"}},
    {"inputs": {"mensagem": "Quero ver o extrato da minha conta"},
     "outputs": {"intencao": "extrato"}},

    # Pagamentos e boletos
    {"inputs": {"mensagem": "Como pagar meu boleto?"},
     "outputs": {"intencao": "pagamento"}},
    {"inputs": {"mensagem": "Quero agendar um pagamento automático"},
     "outputs": {"intencao": "pagamento"}},
]

client.create_examples(dataset_id=dataset.id, examples=examples)

# -----------------------------
# Criação do workflow
# -----------------------------
workflow = create_workflow()

# -----------------------------
# Função target que executa o workflow
# -----------------------------


def target(inputs: dict) -> dict:
    # Cria estado inicial com a mensagem do usuário
    state = FaqState(messages=[HumanMessage(content=inputs["mensagem"])])

    # Executa o workflow
    result = workflow.invoke(state)

    # Se retornou dict, converte de volta para FaqState
    if isinstance(result, dict):
        state = FaqState(**result)
    else:
        state = result

    # Retorna a intenção detectada pelo workflow
    return {"intencao": state.intencao}

# -----------------------------
# Avaliador de corretude
# -----------------------------


def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        model="openai:o3-mini",
        feedback_key="correctness",
    )
    eval_result = evaluator(
        inputs=inputs, outputs=outputs, reference_outputs=reference_outputs
    )
    return eval_result


# -----------------------------
# Executa a avaliação
# -----------------------------
experiment_results = client.evaluate(
    target,
    data=ID_DATASET,
    evaluators=[correctness_evaluator],
    experiment_prefix="experiment-faq-workflow",
    max_concurrency=2,
)
