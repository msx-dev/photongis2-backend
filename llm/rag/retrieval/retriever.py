from dataclasses import dataclass
from typing import Any

from llm.rag.ingestion.chroma import get_manual_collection


@dataclass
class RetrievedChunk:
    content: str
    metadata: dict[str, Any]
    distance: float


def retrieve_manual(
    query: str,
    n_results: int = 5,
) -> list[RetrievedChunk]:

    collection = get_manual_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"] or []
    metadatas = results["metadatas"] or []
    distances = results["distances"] or []

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents[0],
        metadatas[0],
        distances[0],
    ):
        retrieved_chunks.append(
            RetrievedChunk(
                content=document,
                metadata=dict(metadata) if metadata else {},
                distance=distance,
            )
        )

    return retrieved_chunks