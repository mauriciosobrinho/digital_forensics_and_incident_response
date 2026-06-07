import hashlib
import json
from datetime import datetime
from pathlib import Path


def calculate_sha256(
    file_path: Path
) -> str:

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def generate_chain_of_custody(
    file_path: Path,
    output_path: Path,
) -> None:

    sha256_hash = calculate_sha256(file_path)

    payload = {
        "file_name": file_path.name,
        "sha256": sha256_hash,
        "processed_at": datetime.utcnow().isoformat(),
        "processor": "idor-response-platform",
    }

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            payload,
            fp,
            indent=2,
        )
