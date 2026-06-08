from src.agents.graph import (
    build_investigation_graph,
)


def main() -> None:
    graph = build_investigation_graph()

    png = graph.get_graph().draw_mermaid_png()

    output_file = "data/evidence/langgraph_investigation_graph.png"

    with open(
        output_file,
        "wb",
    ) as f:
        f.write(png)

    print(
        f"Graph exported to {output_file}"
    )


if __name__ == "__main__":
    main()