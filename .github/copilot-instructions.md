# Copilot / AI Agent Instructions

Purpose: give AI coding agents concise, actionable knowledge to be immediately productive in this repository.

**Quick start**
- Python: 3.12+; create venv and install: `python -m venv .venv` then `pip install -r requirements.txt`.
- Run pipeline: `python src/app.py`.
- Run tests: `pytest`.

**Big picture**
- Pipeline orchestration is in `src/app.py`: ensure directories, generate chain-of-custody, load logs, parse URIs, persist Parquet.
- Ingestion uses Polars lazy execution: `src/ingestion/loader.py` returns a `pl.LazyFrame`. Processing is done lazily and written with `collect(streaming=True)`.
- Parsing of `uri` fields lives in `src/parsing/uri_parser.py` (regex-based extraction of `invoice_id`, `site_id`, `auth_token`).
- Models are Pydantic v2 data contracts in `src/models/` (e.g., `ParsedEvent` in [src/models/events.py](src/models/events.py)).
- Forensic integrity: `src/ingestion/integrity.py` creates `data/evidence/chain_of_custody.json` (SHA-256 + metadata). The chain-of-custody must be generated before any transformation of raw data.

**Project conventions & patterns**
- Use `pathlib.Path` constants from [src/config/settings.py](src/config/settings.py) for data file locations (`INPUT_CSV`, `PARSED_EVENTS_FILE`, `CHAIN_OF_CUSTODY_FILE`).
- Centralized CSV normalization: `loader.load_logs()` renames malformed CSV headers (notably `http_staus` → `status_code`). Do not rename columns elsewhere; update the loader mapping when CSV changes.
- Polars patterns:
  - Accept and return `pl.LazyFrame` for ingestion/parsing functions.
  - Add columns with `logs.with_columns([...])` using `pl.col(...).str.extract(...).alias(...)` as in `extract_uri_fields()`.
  - Persist with `collect(streaming=True).write_parquet(output_file)` to avoid memory spikes.
- Pydantic models are simple BaseModel classes used as contracts; add new feature schemas under `src/models/` (see `features.py`).

**For code changes**
- If touching raw data ingestion or CSV layout: update `src/ingestion/loader.py` rename map and regenerate `chain_of_custody.json`.
- When adding a new derived column or feature, prefer implementing it as a Polars expression in `parsing` or a new module that returns a `LazyFrame`.
- Preserve streaming/lazy patterns; tests assume `scan_csv` + lazy transforms.

**Tests & debugging**
- Existing tests: `tests/test_integrity.py`, `tests/test_uri_parser.py` — run `pytest` locally.
- Use small subsets of `data/raw/three_months.empty.csv` for fast local iterations.

**Integration & outputs**
- Outputs live in `data/processed/parsed_events.parquet` and evidence in `data/evidence/chain_of_custody.json`.
- Parquet schema is columnar; downstream features expect typed columns (e.g., `invoice_id` as integer).

Examples (patterns to copy)
- Rename mapping (loader):

```py
.rename({"http_staus": "status_code", "http_uri": "uri"})
```

- URI extraction (parsing):

```py
pl.col("uri").str.extract(r"invoice_id=(\d+)", 1).cast(pl.Int64).alias("invoice_id")
```

If anything in this file is unclear or you'd like additional examples (e.g., adding a new feature pipeline, or a recommended testing harness), tell me which area to expand.
