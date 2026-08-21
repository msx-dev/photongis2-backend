from llm.rag.retrieval.answerer import build_context
from llm.rag.retrieval.retriever import retrieve_manual


def main():
    query = "Can I delete a panel connected to an inverter string?"

    chunks = retrieve_manual(
        query=query,
        n_results=3,
    )

    context = build_context(chunks)

    print("CONTEXT")
    print("=" * 80)
    print(context)


if __name__ == "__main__":
    main()