import chromadb
from llm.rag.config import CHROMA_PATH

def get_chroma_client():
    return chromadb.PersistentClient(
        path=CHROMA_PATH,
    )