import json

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_EVAL_RESULTS_FILE,
    AGENT_EVAL_SUMMARY_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_QUESTION_BANK_FILE,
)

from src.evaluation.agent_evaluator import (
    evaluate_agents,
)
from src.evaluation.evaluation_report import (
    build_evaluation_report,
    save_evaluation_summary_csv,
    save_json,
)
from src.evaluation.question_bank import (
    build_agent_question_bank,
)


def _load_json(path):
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def run_agent_evaluation() -> dict:

    question_bank = build_agent_question_bank()

    investigation = _load_json(
        AGENT_INVESTIGATION_FILE
    )

    decision_log = _load_json(
        AGENT_DECISION_LOG_FILE
    )

    evaluation_results = evaluate_agents(
        investigation=investigation,
        decision_log=decision_log,
    )

    evaluation_report = build_evaluation_report(
        evaluation_results
    )

    save_json(
        question_bank,
        AGENT_QUESTION_BANK_FILE,
    )

    save_json(
        evaluation_results,
        AGENT_EVAL_RESULTS_FILE,
    )

    save_json(
        evaluation_report,
        AGENT_EVAL_REPORT_FILE,
    )

    save_evaluation_summary_csv(
        evaluation_results,
        AGENT_EVAL_SUMMARY_FILE,
    )

    return evaluation_report


def main() -> None:
    report = run_agent_evaluation()

    summary = report["summary"]

    print("\nAgent Evaluation completed.")
    print(
        f"Coverage: {summary['overall_coverage_percent']}%"
    )
    print(
        f"Passed: {summary['passed']} | "
        f"Partial: {summary['partial']} | "
        f"Failed: {summary['failed']}"
    )


if __name__ == "__main__":
    main()