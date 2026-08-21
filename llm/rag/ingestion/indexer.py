from pathlib import Path

from llm.rag.config import MANUAL_PATH
from llm.rag.ingestion.loader import load_manual
from llm.rag.ingestion.chunker import chunk_documents
from llm.rag.ingestion.chroma import get_manual_collection


def index_manual() -> None:
    """
    Load the application manual, split it into chunks,
    and store the chunks in Chroma.
    """

    # 1. Make sure the PDF exists
    manual_path = Path(MANUAL_PATH)

    if not manual_path.exists():
        raise FileNotFoundError(
            f"Manual not found: {manual_path}"
        )

    # 2. Load the PDF
    documents = load_manual()

    print(f"Loaded {len(documents)} pages.")

    # 3. Split pages into chunks
    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # 4. Get our persistent Chroma collection
    collection = get_manual_collection()

    # 5. Add chunks to Chroma
    collection.add(
        ids=[
            f"manual-chunk-{index}"
            for index in range(len(chunks))
        ],
        documents=[
            chunk.page_content
            for chunk in chunks
        ],
        metadatas=[
            chunk.metadata
            for chunk in chunks
        ],
    )

    print(f"Stored {len(chunks)} chunks in Chroma.")