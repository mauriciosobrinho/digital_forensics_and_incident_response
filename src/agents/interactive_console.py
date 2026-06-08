import json
from datetime import datetime, timezone

from src.agents.soc_assistant import (
    answer_soc_question,
)

from src.config.settings import (
    INTERACTIVE_SESSION_LOG_FILE,
)


def _append_session_log(
    question: str,
    response: dict,
) -> None:
    if INTERACTIVE_SESSION_LOG_FILE.exists():
        with INTERACTIVE_SESSION_LOG_FILE.open(
            "r",
            encoding="utf-8",
        ) as f:
            log = json.load(f)
    else:
        log = []

    log.append(
        {
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "question": question,
            "response": response,
        }
    )

    INTERACTIVE_SESSION_LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with INTERACTIVE_SESSION_LOG_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            log,
            f,
            indent=2,
            ensure_ascii=False,
        )


def main() -> None:
    print("\nDFIR SOC Interactive Agent Console")
    print("=" * 80)
    print("Examples:")
    print("- Quais são os top IPs atacantes?")
    print("- Qual foi a janela do ataque?")
    print("- Explique IDOR e Broken Access Control")
    print("- Simule bloquear o IP crítico")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nSOC> ").strip()

        if question.lower() in {
            "exit",
            "quit",
            "sair",
        }:
            break

        response = answer_soc_question(
            question
        )

        _append_session_log(
            question,
            response,
        )

        print(
            json.dumps(
                response,
                indent=2,
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()