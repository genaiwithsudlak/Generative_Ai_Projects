
# Handles embeddings and vectorstore creation / loading
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMB_MODEL)

def create_faiss_from_docs(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)

def load_or_create_chroma(persist_dir, docs=None, embeddings=None):
    if os.path.exists(persist_dir) and embeddings is not None:
        return Chroma(embedding_function=embeddings, persist_directory=persist_dir)
    if docs is not None and embeddings is not None:
        return Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_dir)
    return None
