import os
import json
import warnings
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import openai
from dotenv import load_dotenv

# ------------------------------
# 0. Carregar variáveis de ambiente
# ------------------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # configure sua chave

# ------------------------------
# 1. Silenciar avisos do Transformers
# ------------------------------
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# ------------------------------
# 2. Defina a pasta local do modelo
# ------------------------------
CAMINHO_MODELO = "./modelos/bart-large-cnn"

# ------------------------------
# 3. Baixar ou carregar do cache local
# ------------------------------
if not os.path.exists(CAMINHO_MODELO):
    print("Modelo não encontrado na pasta local. Baixando...")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    tokenizer.save_pretrained(CAMINHO_MODELO)

    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    model.config.forced_bos_token_id = 0
    model.save_pretrained(CAMINHO_MODELO)
    print(f"Modelo salvo em {CAMINHO_MODELO}")
else:
    print("Carregando modelo do cache local...")
    tokenizer = AutoTokenizer.from_pretrained(CAMINHO_MODELO)
    model = AutoModelForSeq2SeqLM.from_pretrained(CAMINHO_MODELO)
    model.config.forced_bos_token_id = 0

# ------------------------------
# 4. Pipeline de BART para pré-resumo (CPU)
# ------------------------------
summarizer = pipeline("summarization", model=model,
                      tokenizer=tokenizer, device=-1)


def resumir_bart(texto, min_length=20, max_ratio=0.5):
    input_length = len(tokenizer.encode(texto, truncation=False))
    max_len = max(min_length, int(input_length * max_ratio))
    resumo = summarizer(texto, max_length=max_len,
                        min_length=min_length, do_sample=False)
    return resumo[0]['summary_text']

# ------------------------------
# 5. Função para refinar resumo via OpenAI
# ------------------------------


def refinar_resumo_openai(resumo_bart):
    prompt = f"""
Você é um assistente de resumo de notícias. 
Recebi o seguinte resumo inicial de um artigo:

{resumo_bart}

Tarefas:
1. Reescreva este resumo de forma mais clara, concisa e jornalística.
2. Crie um título chamativo de até 10 palavras.
3. Liste 3-5 insights principais do artigo.

Retorne em JSON com os campos: "titulo", "resumo", "insights".
"""

    response = openai.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    conteudo = response.choices[0].message.content
    return conteudo


# ------------------------------
# 6. Ler arquivo noticias.json e processar
# ------------------------------
JSON_FILE = "noticias.json"
OUTPUT_JSON = "resumos_noticias_openai.json"
OUTPUT_HTML = "resumos_noticias.html"

if not os.path.exists(JSON_FILE):
    print(f"Arquivo {JSON_FILE} não encontrado!")
else:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    resumos = []

    for idx, noticia in enumerate(noticias, 1):
        conteudo = noticia.get("conteudo", "")
        url = noticia.get("url", "")
        titulo = noticia.get("titulo", f"Notícia {idx}")

        if not conteudo.strip():
            continue

        # 1️⃣ Pré-resumo com BART
        resumo_bart = resumir_bart(conteudo)

        # 2️⃣ Refinamento com LLM OpenAI (resumo final)
        resumo_refinado_json = refinar_resumo_openai(resumo_bart)

        print(f"\n[{idx}] {titulo}")
        print(f"URL: {url}")
        print("Resumo final (JSON do LLM):")
        print(resumo_refinado_json)

        resumos.append({
            "titulo_original": titulo,
            "url": url,
            "resumo_final": resumo_refinado_json
        })

    # Salvar JSON com resumos refinados
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(resumos, f, ensure_ascii=False, indent=2)

    print(f"\nTodos os resumos refinados salvos em {OUTPUT_JSON}")

    # ------------------------------
    # 7. Gerar HTML com Bootstrap
    # ------------------------------
    HTML_HEAD = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resumos de Notícias</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container my-5">
    <h1 class="mb-4">Resumos de Notícias</h1>
    <div class="row row-cols-1 row-cols-md-2 g-4">
"""

    HTML_FOOT = """
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

    def gerar_card(noticia):
        titulo_original = noticia.get(
            "titulo_original", "Título não disponível")
        url = noticia.get("url", "#")
        resumo_json = noticia.get("resumo_final", "{}")

        try:
            resumo_dict = json.loads(resumo_json)
            titulo = resumo_dict.get("titulo", titulo_original)
            resumo = resumo_dict.get("resumo", "Resumo não disponível")
        except:
            titulo = titulo_original
            resumo = resumo_json

        card_html = f"""
        <div class="col">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">{titulo}</h5>
                    <p class="card-text">{resumo}</p>
                    <a href="{url}" target="_blank" class="btn btn-primary">Ler notícia</a>
                </div>
            </div>
        </div>
        """
        return card_html

    cards_html = "\n".join([gerar_card(n) for n in resumos])
    html_completo = HTML_HEAD + cards_html + HTML_FOOT

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_completo)

    print(f"HTML gerado com sucesso: {OUTPUT_HTML}")
