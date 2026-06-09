import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_evaluation_report(
    evaluation_results: dict[str, Any],
) -> dict[str, Any]:

    results = evaluation_results["results"]

    by_agent: dict[str, list[dict[str, Any]]] = {}

    for item in results:
        by_agent.setdefault(
            item["agent"],
            [],
        ).append(item)

    agent_scores = {}

    for agent, items in by_agent.items():
        avg_score = sum(
            item["score"]
            for item in items
        ) / len(items)

        agent_scores[agent] = {
            "questions": len(items),
            "average_score": round(
                avg_score,
                4,
            ),
            "coverage_percent": round(
                avg_score * 100,
                2,
            ),
            "passed": sum(
                1
                for item in items
                if item["status"] == "passed"
            ),
            "partial": sum(
                1
                for item in items
                if item["status"] == "partial"
            ),
            "failed": sum(
                1
                for item in items
                if item["status"] == "failed"
            ),
        }

    overall_score = sum(
        item["score"]
        for item in results
    ) / len(results)

    return {
        "report_type": "agent_evaluation_report",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "summary": {
            "total_questions": len(results),
            "overall_score": round(
                overall_score,
                4,
            ),
            "overall_coverage_percent": round(
                overall_score * 100,
                2,
            ),
            "passed": sum(
                1
                for item in results
                if item["status"] == "passed"
            ),
            "partial": sum(
                1
                for item in results
                if item["status"] == "partial"
            ),
            "failed": sum(
                1
                for item in results
                if item["status"] == "failed"
            ),
        },
        "agent_scores": agent_scores,
        "coverage_statement": (
            "This evaluation validates whether each agent output contains "
            "the minimum evidence required by the technical challenge."
        ),
    }


def save_json(
    data: dict[str, Any] | list[dict[str, Any]],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def save_evaluation_summary_csv(
    evaluation_results: dict[str, Any],
    path: Path,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = evaluation_results["results"]

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "agent",
                "question",
                "challenge_requirement",
                "score",
                "status",
                "passed_checks",
                "total_checks",
            ],
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    "id": row["id"],
                    "agent": row["agent"],
                    "question": row["question"],
                    "challenge_requirement": row[
                        "challenge_requirement"
                    ],
                    "score": row["score"],
                    "status": row["status"],
                    "passed_checks": row[
                        "passed_checks"
                    ],
                    "total_checks": row[
                        "total_checks"
                    ],
                }
            )