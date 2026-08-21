import os

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "./chroma_data",
)

MANUAL_PATH = os.getenv(
    "MANUAL_PATH",
    "docs/solar_manual.pdf",
)

MANUAL_COLLECTION_NAME = os.getenv(
    "MANUAL_COLLECTION_NAME",
    "solar_manual",
)