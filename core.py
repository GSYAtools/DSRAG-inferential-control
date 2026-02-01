import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

# --- FUNCIONES BASE ---

def load_documents(data_dirs):
    """Carga documentos desde una o varias carpetas de DPs"""
    docs = []
    for data_dir in data_dirs:
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                path = os.path.join(data_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    docs.append(Document(page_content=content, metadata={
                        "source": filename,
                        "dp": os.path.basename(data_dir)
                    }))
    return docs

def create_faiss_index(documents, index_dir):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(index_dir)

def query_index(index_dir, query, top_k=3):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(query, k=top_k)
    return results
