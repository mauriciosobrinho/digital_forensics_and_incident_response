import json
from pathlib import Path
from typing import Any

from src.rag.knowledge_base import (
    load_knowledge_documents,
)

from src.rag.retriever import (
    retrieve_context,
)


def build_rag_context(
    knowledge_dir: Path,
    query: str,
    top_k: int = 3,
) -> dict[str, Any]:
    documents = load_knowledge_documents(
        knowledge_dir
    )

    retrieved = retrieve_context(
        query=query,
        documents=documents,
        top_k=top_k,
    )

    return {
        "query": query,
        "top_k": top_k,
        "retrieved_documents": [
            {
                "source": item["source"],
                "title": item["title"],
                "score": item["score"],
                "content_preview": item["content"][:1200],
            }
            for item in retrieved
        ],
    }


def save_rag_context(
    rag_context: dict[str, Any],
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            rag_context,
            f,
            indent=2,
            ensure_ascii=False,
        )