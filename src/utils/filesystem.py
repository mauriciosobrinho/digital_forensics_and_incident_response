from pathlib import Path


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_project_directories() -> None:

    from src.config.settings import (
        PROCESSED_DIR,
        EVIDENCE_DIR,
    )

    ensure_directory(PROCESSED_DIR)
    ensure_directory(EVIDENCE_DIR)
