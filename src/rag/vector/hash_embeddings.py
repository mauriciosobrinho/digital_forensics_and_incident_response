from __future__ import annotations

import hashlib
import math
import re
from typing import Any


class HashEmbeddingFunction:
    def __init__(
        self,
        dimensions: int = 384,
    ) -> None:
        self.dimensions = dimensions

    def name(self) -> str:
        return "dfir_hash_embedding"

    def __call__(
        self,
        input: list[str],
    ) -> list[list[float]]:
        return [
            self.embed_text(text)
            for text in input
        ]

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [
            self.embed_text(text)
            for text in texts
        ]

    def embed_query(
        self,
        text: str | None = None,
        input: str | list[str] | None = None,
    ) -> list[float] | list[list[float]]:
        query = text if text is not None else input

        if isinstance(query, list):
            return [
                self.embed_text(item)
                for item in query
            ]

        if query is None:
            return self.embed_text("")

        return self.embed_text(query)

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        vector = [0.0] * self.dimensions

        tokens = re.findall(
            r"[a-zA-Z0-9_./:-]+",
            text.lower(),
        )

        for token in tokens:
            digest = hashlib.sha256(
                token.encode("utf-8")
            ).hexdigest()

            index = int(digest[:8], 16) % self.dimensions
            sign = 1.0 if int(digest[8:10], 16) % 2 == 0 else -1.0

            vector[index] += sign

        norm = math.sqrt(
            sum(value * value for value in vector)
        )

        if norm == 0:
            return vector

        return [
            value / norm
            for value in vector
        ]