from pathlib import Path

import matplotlib.pyplot as plt


def save_bar_chart(
    *,
    labels: list[str],
    values: list[float],
    title: str,
    ylabel: str,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def generate_report_figures(
    *,
    platform_metrics: dict,
    agent_metrics: dict,
    evaluation_report: dict,
    output_dir: Path,
) -> dict[str, str]:

    figures = {}

    pipeline = platform_metrics.get("pipeline_metrics", {})

    path = output_dir / "pipeline_metrics.png"
    save_bar_chart(
        labels=[
            "Logs",
            "IPs",
            "IDOR",
            "Anomalous IPs",
            "IOCs",
        ],
        values=[
            pipeline.get("n_logs_processed", 0),
            pipeline.get("n_ips_analyzed", 0),
            pipeline.get("n_idor_findings", 0),
            pipeline.get("n_anomalous_ips", 0),
            pipeline.get("n_iocs_generated", 0),
        ],
        title="Pipeline Metrics",
        ylabel="Count",
        output_path=path,
    )
    figures["pipeline_metrics"] = str(path)

    agent_scores = evaluation_report.get("agent_scores", {})
    path = output_dir / "agent_coverage.png"
    save_bar_chart(
        labels=list(agent_scores.keys()),
        values=[
            item.get("coverage_percent", 0)
            for item in agent_scores.values()
        ],
        title="Agent Evaluation Coverage",
        ylabel="Coverage (%)",
        output_path=path,
    )
    figures["agent_coverage"] = str(path)

    path = output_dir / "agent_metrics.png"
    save_bar_chart(
        labels=[
            "Decisions",
            "Workflow Events",
            "Human Approvals",
            "Tool Calls",
            "Dry-run Actions",
        ],
        values=[
            agent_metrics.get("n_agent_decisions", 0),
            agent_metrics.get("n_workflow_events", 0),
            agent_metrics.get("n_human_approvals", 0),
            agent_metrics.get("n_tool_calls", 0),
            agent_metrics.get("n_dry_run_actions", 0),
        ],
        title="Agent & Workflow Metrics",
        ylabel="Count",
        output_path=path,
    )
    figures["agent_metrics"] = str(path)

    return figures