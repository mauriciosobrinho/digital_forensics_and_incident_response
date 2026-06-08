from typing import Any


def _score_document(
    query: str,
    content: str,
) -> int:
    query_terms = {
        term.lower().strip()
        for term in query.split()
        if len(term.strip()) > 2
    }

    content_lower = content.lower()

    return sum(
        1
        for term in query_terms
        if term in content_lower
    )


def retrieve_context(
    query: str,
    documents: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    scored = []

    for doc in documents:
        score = _score_document(
            query=query,
            content=doc["content"],
        )

        scored.append(
            {
                **doc,
                "score": score,
            }
        )

    return [
        item
        for item in sorted(
            scored,
            key=lambda x: x["score"],
            reverse=True,
        )
        if item["score"] > 0
    ][:top_k]