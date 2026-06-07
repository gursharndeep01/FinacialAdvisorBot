from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
from langchain_huggingface import HuggingFaceEmbeddings
from config import DATA_PATH, FAISS_PATH


def build_index():
    # Load PDF documents
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"batch_size": 8}  
    )
    # Build FAISS index
    db = FAISS.from_documents(chunks, embeddings)
    # Save the index to disk
    db.save_local(FAISS_PATH)
    print("Index built and saved to disk.", len(chunks))
def load_index():
    # Load the FAISS index from disk
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    return db

_db = None
def get_db():
    global _db
    if _db is None:
        print("Loading FAISS index into memory...")
        _db = load_index()
        print("Index loaded!")
    return _db

def get_relevant_chunks(query, k=4):
    # Retrieve relevant chunks from the index
    db = get_db()
    results = db.similarity_search(query, k=k)
    return results