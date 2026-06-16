import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class EmbeddingSettings:
    vector_store_backend: str
    embedding_provider: str
    collection_name: str
    persist_directory: str
    embedding_dimensions: int


def load_embedding_settings() -> EmbeddingSettings:
    return EmbeddingSettings(
        vector_store_backend=os.getenv(
            "VECTOR_STORE_BACKEND",
            "chroma",
        ),
        embedding_provider=os.getenv(
            "EMBEDDING_PROVIDER",
            "hash",
        ),
        collection_name=os.getenv(
            "VECTOR_STORE_COLLECTION",
            "dfir_investigation_artifacts",
        ),
        persist_directory=os.getenv(
            "VECTOR_STORE_DIR",
            "data/vector_store/chroma",
        ),
        embedding_dimensions=int(
            os.getenv(
                "EMBEDDING_DIMENSIONS",
                "384",
            )
        ),
    )