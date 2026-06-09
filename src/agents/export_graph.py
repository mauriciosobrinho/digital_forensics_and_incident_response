from pathlib import Path

from src.agents.graph import (
    build_investigation_graph,
)

from src.config.settings import (
    LANGGRAPH_WORKFLOW_FILE,
    LANGGRAPH_WORKFLOW_MERMAID_FILE,
)


def export_langgraph_workflow() -> dict:

    graph = build_investigation_graph()

    LANGGRAPH_WORKFLOW_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = {
        "png_generated": False,
        "png_file": str(LANGGRAPH_WORKFLOW_FILE),
        "mermaid_generated": False,
        "mermaid_file": str(LANGGRAPH_WORKFLOW_MERMAID_FILE),
        "fallback_used": False,
        "error": None,
    }

    try:
        png = graph.get_graph().draw_mermaid_png()

        with LANGGRAPH_WORKFLOW_FILE.open(
            "wb",
        ) as f:
            f.write(png)

        result["png_generated"] = True

    except Exception as exc:
        result["fallback_used"] = True
        result["error"] = str(exc)

    finally:
        mermaid = graph.get_graph().draw_mermaid()

        with LANGGRAPH_WORKFLOW_MERMAID_FILE.open(
            "w",
            encoding="utf-8",
        ) as f:
            f.write(mermaid)

        result["mermaid_generated"] = True

    return result


def main() -> None:
    result = export_langgraph_workflow()

    if result["png_generated"]:
        print(
            f"PNG graph exported to {result['png_file']}"
        )
    else:
        print(
            "PNG graph rendering failed. "
            f"Mermaid fallback exported to {result['mermaid_file']}"
        )

        if result["error"]:
            print(
                f"Render error: {result['error']}"
            )


if __name__ == "__main__":
    main()