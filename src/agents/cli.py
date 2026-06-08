import json
from pathlib import Path

from src.agents.runner import (
    run_agent_investigation,
)

from src.config.settings import (
    AGENT_INVESTIGATION_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    HUMAN_APPROVAL_REQUEST_FILE,
)


def _print_json_file(
    file_path: Path,
) -> None:
    with file_path.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    print(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> None:
    print("\nDFIR LangGraph Agent Console")
    print("=" * 80)
    print("1 - Run investigation")
    print("2 - Show investigation")
    print("3 - Show response playbook")
    print("4 - Show human approval request")
    print("5 - Show human approval decision")
    print("0 - Exit")

    while True:
        option = input("\nSelect option: ").strip()

        if option == "1":
            run_agent_investigation(
                dry_run=True,
                human_approval_status="pending",
            )
            print("Investigation completed.")

        elif option == "2":
            _print_json_file(
                AGENT_INVESTIGATION_FILE
            )

        elif option == "3":
            _print_json_file(
                AGENT_RESPONSE_PLAYBOOK_FILE
            )

        elif option == "4":
            _print_json_file(
                HUMAN_APPROVAL_REQUEST_FILE
            )

        elif option == "5":
            _print_json_file(
                HUMAN_APPROVAL_DECISION_FILE
            )

        elif option == "0":
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()