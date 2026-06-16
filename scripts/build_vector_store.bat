@echo off
setlocal

echo [build_vector_store] Building Chroma vector store...
python -m src.rag.vector.build_vector_store
if errorlevel 1 exit /b 1

endlocal