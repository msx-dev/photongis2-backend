from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)


def get_embedding_function():
    """
    Return the embedding model used by Chroma.
    """

    return SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2",
    )