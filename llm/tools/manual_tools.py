from langchain.tools import tool

from llm.rag.retrieval.retriever import retrieve_manual


@tool
def search_user_manual(
    query: str,
) -> str:
    """
    Search the solar application user manual for instructions,
    rules, limitations, and information about how the application works.
    """

    results = retrieve_manual(
        query=query,
        n_results=5,
    )

    if not results:
        return "No relevant information was found in the user manual."

    lines: list[str] = []

    for result in results:
        page = result.metadata.get("page")

        if page is not None:
            lines.append(
                f"Source: User Guide, page {page}"
            )
        else:
            lines.append(
                "Source: User Guide"
            )

        lines.append(result.content)
        lines.append("---")

    return "\n".join(lines)