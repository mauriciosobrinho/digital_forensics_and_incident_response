from __future__ import annotations

import json

from src.rag.vector.chroma_store import rebuild_vector_store


def main() -> None:
    result = rebuild_vector_store()

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()