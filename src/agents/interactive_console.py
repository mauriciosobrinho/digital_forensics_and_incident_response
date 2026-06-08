import argparse
import json

from src.agents.soc_assistant import answer_soc_question


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DFIR SOC Interactive Agent Console"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Show raw JSON payloads for debugging.",
    )

    args = parser.parse_args()

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

        if question.lower() in {"exit", "quit", "sair"}:
            break

        response = answer_soc_question(question)

        if args.json:
            print(
                json.dumps(
                    response,
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print("\n" + response["answer"])


if __name__ == "__main__":
    main()