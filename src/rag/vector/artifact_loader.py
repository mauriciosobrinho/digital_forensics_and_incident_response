from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[3]


DEFAULT_ARTIFACT_PATHS = [
    "reports/technical_report.md",
    "reports/evidence_appendix.md",
    "reports/methodology.md",
    "reports/architecture.md",
    "reports/executive_summary.md",
    "data/evidence/forensic_evidence.json",
    "data/evidence/agent_investigation.json",
    "data/evidence/nist_incident_report.json",
    "data/evidence/containment_strategy.json",
    "data/evidence/root_cause_analysis.json",
    "data/observability/soc_dashboard_data.json",
    "data/evaluation/agent_eval_report.json",
    "data/knowledge/idor_playbook.md",
    "data/knowledge/incident_response_policy.md",
]


@dataclass(frozen=True)
class LoadedArtifact:
    source_path: str
    artifact_type: str
    text: str


@dataclass(frozen=True)
class ArtifactChunk:
    chunk_id: str
    source_path: str
    artifact_type: str
    chunk_index: int
    text: str


def _json_to_text(value: Any, prefix: str = "") -> list[str]:
    lines: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            lines.extend(_json_to_text(item, child_prefix))

    elif isinstance(value, list):
        for index, item in enumerate(value):
            child_prefix = f"{prefix}[{index}]"
            lines.extend(_json_to_text(item, child_prefix))

    else:
        lines.append(f"{prefix}: {value}")

    return lines


def load_artifact(
    relative_path: str,
    root_dir: Path = ROOT_DIR,
) -> LoadedArtifact | None:
    path = root_dir / relative_path

    if not path.exists():
        return None

    suffix = path.suffix.lower()

    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        text = "\n".join(_json_to_text(data))
        artifact_type = "json"
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")
        artifact_type = "markdown" if suffix == ".md" else "text"

    if not text.strip():
        return None

    return LoadedArtifact(
        source_path=relative_path,
        artifact_type=artifact_type,
        text=text,
    )


def load_default_artifacts() -> list[LoadedArtifact]:
    artifacts: list[LoadedArtifact] = []

    for path in DEFAULT_ARTIFACT_PATHS:
        artifact = load_artifact(path)

        if artifact:
            artifacts.append(artifact)

    return artifacts


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    clean = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    if len(clean) <= chunk_size:
        return [clean]

    chunks: list[str] = []
    start = 0

    while start < len(clean):
        end = start + chunk_size
        chunk = clean[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(clean):
            break

        start = max(0, end - overlap)

    return chunks


def build_artifact_chunks(
    artifacts: list[LoadedArtifact],
) -> list[ArtifactChunk]:
    chunks: list[ArtifactChunk] = []

    for artifact in artifacts:
        for index, text in enumerate(chunk_text(artifact.text)):
            safe_source = (
                artifact.source_path
                .replace("/", "_")
                .replace("\\", "_")
                .replace(".", "_")
            )

            chunks.append(
                ArtifactChunk(
                    chunk_id=f"{safe_source}_{index}",
                    source_path=artifact.source_path,
                    artifact_type=artifact.artifact_type,
                    chunk_index=index,
                    text=text,
                )
            )

    return chunks