from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

logging.info("Criando pasta local para o modelo...")
model_dir = "./models/all-MiniLM-L6-v2"
os.makedirs(model_dir, exist_ok=True)

logging.info("Carregando modelo SentenceTransformer...")
model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=model_dir)

logging.info("Preparando base de conhecimento...")
documents = [
    {"chunk": "Nosso horário é de segunda a sexta, 09h-18h.", "source": "FAQ-Atendimento"},
    {"chunk": "Para cancelar, vá em Conta > Assinaturas > Cancelar.", "source": "FAQ-Cancelamento"},
    {"chunk": "Oferecemos suporte via chat, e-mail e telefone.", "source": "FAQ-Suporte"},
    {"chunk": "Planos podem ser atualizados diretamente na página de Assinaturas.", "source": "FAQ-Planos"},
]

texts = [doc["chunk"] for doc in documents]

logging.info("Gerando embeddings para os documentos...")
embeddings = model.encode(texts, convert_to_numpy=True)

logging.info("Indexando vetores no FAISS...")
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
faiss.normalize_L2(embeddings)
index.add(embeddings)

logging.info("Pipeline de RAG pronto.")

def query_rag(question, k=2):
    logging.info(f"Consultando base para a pergunta: '{question}'")
    q_emb = model.encode([question])
    faiss.normalize_L2(q_emb)
    
    D, I = index.search(np.array(q_emb), k=k)
    results = []
    for idx in I[0]:
        results.append({
            "chunk": documents[idx]["chunk"],
            "source": documents[idx]["source"]
        })
    logging.info(f"Encontrados {len(results)} trechos relevantes.")
    return results

question = "Como faço para cancelar minha assinatura?"
top_chunks = query_rag(question, k=2)

print(f"\nPergunta: {question}\n")
print("Trechos mais relevantes:")
for i, r in enumerate(top_chunks, 1):
    print(f"{i}. {r['chunk']} (Fonte: {r['source']})")
