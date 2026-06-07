from src.config.settings import (
    INPUT_CSV,
    PARSED_EVENTS_FILE,
    CHAIN_OF_CUSTODY_FILE,
)

from src.utils.filesystem import (
    ensure_project_directories,
)

from src.ingestion.loader import (
    load_logs,
)

from src.ingestion.integrity import (
    generate_chain_of_custody,
)

from src.parsing.uri_parser import (
    extract_uri_fields,
    persist_parsed_events,
)


def run_pipeline() -> None:

    ensure_project_directories()

    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    logs = load_logs(INPUT_CSV)

    parsed_events = extract_uri_fields(logs)

    persist_parsed_events(
        parsed_events,
        PARSED_EVENTS_FILE,
    )

    print(
        "Sprint 1.1 concluído com sucesso."
    )


if __name__ == "__main__":
    run_pipeline()
