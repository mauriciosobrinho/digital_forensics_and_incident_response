from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config.embedding_settings import load_embedding_settings
from src.rag.vector.artifact_loader import (
    build_artifact_chunks,
    load_default_artifacts,
)
from src.rag.vector.hash_embeddings import HashEmbeddingFunction


ROOT_DIR = Path(__file__).resolve().parents[3]


def _get_collection():
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "chromadb is not installed. Run: pip install -r requirements.txt"
        ) from exc

    settings = load_embedding_settings()

    persist_dir = ROOT_DIR / settings.persist_directory
    persist_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(persist_dir),
    )

    embedding_function = HashEmbeddingFunction(
        dimensions=settings.embedding_dimensions,
    )

    return client.get_or_create_collection(
        name=settings.collection_name,
        embedding_function=embedding_function,
        metadata={
            "description": "DFIR semantic and investigative artifacts",
        },
    )


def rebuild_vector_store() -> dict[str, Any]:
    collection = _get_collection()

    artifacts = load_default_artifacts()
    chunks = build_artifact_chunks(artifacts)

    existing = collection.get()
    existing_ids = existing.get("ids", [])

    if existing_ids:
        collection.delete(ids=existing_ids)

    if chunks:
        collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "source_path": chunk.source_path,
                    "artifact_type": chunk.artifact_type,
                    "chunk_index": chunk.chunk_index,
                }
                for chunk in chunks
            ],
        )

    settings = load_embedding_settings()

    return {
        "backend": settings.vector_store_backend,
        "embedding_provider": settings.embedding_provider,
        "collection": settings.collection_name,
        "persist_directory": settings.persist_directory,
        "artifacts_loaded": len(artifacts),
        "chunks_indexed": len(chunks),
        "sources": [artifact.source_path for artifact in artifacts],
    }


def query_vector_store(
    query: str,
    top_k: int = 6,
) -> dict[str, Any]:
    collection = _get_collection()

    result = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    retrieved = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved.append(
            {
                "content": document,
                "source_path": metadata.get("source_path"),
                "artifact_type": metadata.get("artifact_type"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )

    return {
        "query": query,
        "top_k": top_k,
        "retrieved_documents": retrieved,
    }