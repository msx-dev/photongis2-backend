import chromadb

from typing import cast

from chromadb.api.types import (
    EmbeddingFunction,
    Embeddable,
)

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

from llm.rag.config import (
    CHROMA_PATH,
    MANUAL_COLLECTION_NAME,
)


# ---------------------------------------------------------------------------
# EMBEDDING FUNCTION
# ---------------------------------------------------------------------------

embedding_function = cast(
    EmbeddingFunction[Embeddable],
    SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2",
    ),
)


# ---------------------------------------------------------------------------
# CHROMA CLIENT
# ---------------------------------------------------------------------------

def get_chroma_client():
    """
    Return the persistent Chroma client.
    """

    return chromadb.PersistentClient(
        path=CHROMA_PATH,
    )


# ---------------------------------------------------------------------------
# MANUAL COLLECTION
# ---------------------------------------------------------------------------

def get_manual_collection():
    """
    Return the Chroma collection used for the application manual.
    """

    client = get_chroma_client()

    return client.get_or_create_collection(
        name=MANUAL_COLLECTION_NAME,
        embedding_function=embedding_function,
    )


# ---------------------------------------------------------------------------
# RESET MANUAL COLLECTION
# ---------------------------------------------------------------------------

def reset_manual_collection():
    """
    Delete the existing manual collection and create a fresh one.
    """

    client = get_chroma_client()

    try:
        client.delete_collection(
            name=MANUAL_COLLECTION_NAME,
        )
    except Exception:
        pass

    return client.get_or_create_collection(
        name=MANUAL_COLLECTION_NAME,
        embedding_function=embedding_function,
    )