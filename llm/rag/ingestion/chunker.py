from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_documents(
    documents: list[Document],
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )
    #split_documents keeps the metadata from Document objects!
    return splitter.split_documents(documents)