from pathlib import Path
from typing import Any


def load_knowledge_documents(
    knowledge_dir: Path,
) -> list[dict[str, Any]]:
    if not knowledge_dir.exists():
        return []

    documents = []

    for file_path in sorted(
        knowledge_dir.glob("*.md")
    ):
        documents.append(
            {
                "source": str(file_path),
                "title": file_path.stem,
                "content": file_path.read_text(
                    encoding="utf-8"
                ),
            }
        )

    return documents