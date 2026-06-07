from pathlib import Path

from src.ingestion.integrity import (
    calculate_sha256,
)


def test_sha256():

    temp_file = Path(
        "temp_test.txt"
    )

    temp_file.write_text(
        "hello world"
    )

    result = calculate_sha256(
        temp_file
    )

    assert len(result) == 64

    temp_file.unlink()
