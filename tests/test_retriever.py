from llm.rag.retrieval.retriever import retrieve_manual


def main():
    query = "Can I delete a panel connected to an inverter string?"

    results = retrieve_manual(
        query=query,
        n_results=5,
    )

    print("Results:")
    print("=" * 80)

    for index, result in enumerate(results):
        print(f"\nRESULT {index + 1}")
        print("-" * 80)

        print(f"Distance: {result.distance}")
        print(f"Page: {result.metadata.get('page')}")

        print("\nContent:")
        print(result.content)


if __name__ == "__main__":
    main()