from llm.rag.retrieval.retriever import RetrievedChunk


def build_context(
    chunks: list[RetrievedChunk],
) -> str:
    """
    Convert retrieved chunks into context for the LLM.
    """

    context_parts = []

    for chunk in chunks:
        page = chunk.metadata.get("page_label")

        context_parts.append(
            f"Source: User Guide, page {page}\n"
            f"{chunk.content}"
        )

    return "\n\n---\n\n".join(context_parts)