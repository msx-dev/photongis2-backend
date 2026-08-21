from llm.rag.ingestion.chunker import chunk_documents
from llm.rag.ingestion.loader import load_manual


def main():
    documents = load_manual()

    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} pages.")
    print(f"Created {len(chunks)} chunks.")
    print()

    for index, chunk in enumerate(chunks, start=1):
        print("=" * 80)
        print(f"CHUNK {index}")
        print(f"Length: {len(chunk.page_content)} characters")
        print(f"Metadata: {chunk.metadata}")
        print()
        print(chunk.page_content)


if __name__ == "__main__":
    main()