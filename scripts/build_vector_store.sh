#!/usr/bin/env bash
set -euo pipefail

echo "[build_vector_store] Building Chroma vector store..."
python -m src.rag.vector.build_vector_store