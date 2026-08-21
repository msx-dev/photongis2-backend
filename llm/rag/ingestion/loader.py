from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


PDF_PATH = Path("docs/solar_manual.pdf")


def load_manual():
    loader = PyPDFLoader(str(PDF_PATH))

    documents = loader.load()

    return documents