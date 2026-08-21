from llm.rag.ingestion.loader import load_manual

documents = load_manual()

print(f"Loaded {len(documents)} pages.")

for document in documents:
    print("=" * 80)
    print(document.metadata)
    print(document.page_content[:500])