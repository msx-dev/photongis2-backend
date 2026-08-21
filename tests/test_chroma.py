from llm.rag.client import get_chroma_client


def main():
    client = get_chroma_client()

    collection = client.get_collection(
        name="test_collection",
    )

    result = collection.get(
        ids=["test-1"],
    )

    print(result)


if __name__ == "__main__":
    main()