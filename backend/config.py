import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"
DATA_PATH = os.path.join(BASE_DIR, "../data/")
FAISS_PATH = os.path.join(BASE_DIR, "../faiss_index/")