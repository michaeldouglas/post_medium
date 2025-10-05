from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app import MongoConnection

model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1", trust_remote_code=True)


def get_embedding(data):
    """Criar embeddings vetoriais para os dados fornecidos."""
    embedding = model.encode(data)
    return embedding.tolist()


loader = PyPDFLoader("app/artigo_patricia.pdf")
data = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400, chunk_overlap=20)
documents = text_splitter.split_documents(data)

docs_to_insert = [{
    "text": doc.page_content,
    "embedding": get_embedding(doc.page_content)
} for doc in documents]


connection = MongoConnection()
client = connection.get_client()

collection = client["artigo_db"]["base_conhecimento"]

result = collection.insert_many(docs_to_insert)
