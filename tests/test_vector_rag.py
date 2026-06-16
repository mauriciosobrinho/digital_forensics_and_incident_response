from src.rag.vector.artifact_loader import (
    LoadedArtifact,
    build_artifact_chunks,
    chunk_text,
)
from src.rag.vector.hash_embeddings import HashEmbeddingFunction


def test_chunk_text():
    chunks = chunk_text(
        "A" * 3000,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) > 1


def test_build_artifact_chunks():
    chunks = build_artifact_chunks(
        [
            LoadedArtifact(
                source_path="reports/test.md",
                artifact_type="markdown",
                text="Patient zero evidence and IDOR investigation.",
            )
        ]
    )

    assert len(chunks) == 1
    assert chunks[0].source_path == "reports/test.md"


def test_hash_embedding_is_deterministic():
    embedding = HashEmbeddingFunction(dimensions=32)

    first = embedding.embed_text("IDOR patient zero evidence")
    second = embedding.embed_text("IDOR patient zero evidence")

    assert first == second
    assert len(first) == 32