from llm.rag.ingestion.chroma import get_manual_collection


def main():
    collection = get_manual_collection()

    print("Collection name:", collection.name)
    print("Document count:", collection.count())


if __name__ == "__main__":
    main()