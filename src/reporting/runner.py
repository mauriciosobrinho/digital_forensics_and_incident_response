from src.config.settings import (
    AGENT_EVAL_REPORT_FILE,
    AGENT_METRICS_FILE,
    ARCHITECTURE_MD_FILE,
    CONTAINMENT_STRATEGY_FILE,
    EVIDENCE_APPENDIX_MD_FILE,
    EXECUTIVE_SUMMARY_MD_FILE,
    EXECUTIVE_SUMMARY_PDF_FILE,
    HEALTHCHECK_FILE,
    NIST_INCIDENT_REPORT_FILE,
    PLATFORM_METRICS_FILE,
    REPORT_FIGURES_DIR,
    ROOT_CAUSE_ANALYSIS_FILE,
    SOC_DASHBOARD_DATA_FILE,
    TECHNICAL_REPORT_MD_FILE,
    TECHNICAL_REPORT_PDF_FILE,
)
from src.reporting.figures import (
    generate_report_figures,
)
from src.reporting.markdown_builder import (
    build_architecture_doc,
    build_evidence_appendix,
    build_executive_summary,
    build_methodology_doc,
    build_technical_report,
)
from src.reporting.pdf_exporter import (
    export_markdown_to_pdf,
)
from src.reporting.report_data_loader import (
    load_json,
)
from src.config.settings import (
    METHODOLOGY_MD_FILE,
)


def _save_text(
    text: str,
    path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_text(
        text,
        encoding="utf-8",
    )


def run_reporting() -> dict:

    nist_report = load_json(
        NIST_INCIDENT_REPORT_FILE,
        {},
    )

    platform_metrics = load_json(
        PLATFORM_METRICS_FILE,
        {},
    )

    agent_metrics = load_json(
        AGENT_METRICS_FILE,
        {},
    )

    evaluation_report = load_json(
        AGENT_EVAL_REPORT_FILE,
        {},
    )

    healthcheck = load_json(
        HEALTHCHECK_FILE,
        {},
    )

    figures = generate_report_figures(
        platform_metrics=platform_metrics,
        agent_metrics=agent_metrics,
        evaluation_report=evaluation_report,
        output_dir=REPORT_FIGURES_DIR,
    )

    technical_report = build_technical_report(
        nist_report=nist_report,
        platform_metrics=platform_metrics,
        agent_metrics=agent_metrics,
        evaluation_report=evaluation_report,
        healthcheck=healthcheck,
        figures=figures,
    )

    executive_summary = build_executive_summary(
        nist_report=nist_report,
        platform_metrics=platform_metrics,
        evaluation_report=evaluation_report,
    )

    artifacts = {
        "nist_incident_report": str(NIST_INCIDENT_REPORT_FILE),
        "containment_strategy": str(CONTAINMENT_STRATEGY_FILE),
        "root_cause_analysis": str(ROOT_CAUSE_ANALYSIS_FILE),
        "platform_metrics": str(PLATFORM_METRICS_FILE),
        "agent_metrics": str(AGENT_METRICS_FILE),
        "healthcheck": str(HEALTHCHECK_FILE),
        "soc_dashboard_data": str(SOC_DASHBOARD_DATA_FILE),
        "agent_eval_report": str(AGENT_EVAL_REPORT_FILE),
    }

    _save_text(
        technical_report,
        TECHNICAL_REPORT_MD_FILE,
    )

    _save_text(
        executive_summary,
        EXECUTIVE_SUMMARY_MD_FILE,
    )

    _save_text(
        build_architecture_doc(),
        ARCHITECTURE_MD_FILE,
    )

    _save_text(
        build_methodology_doc(),
        METHODOLOGY_MD_FILE,
    )

    _save_text(
        build_evidence_appendix(
            artifacts=artifacts,
        ),
        EVIDENCE_APPENDIX_MD_FILE,
    )

    export_markdown_to_pdf(
        markdown_path=TECHNICAL_REPORT_MD_FILE,
        pdf_path=TECHNICAL_REPORT_PDF_FILE,
    )

    export_markdown_to_pdf(
        markdown_path=EXECUTIVE_SUMMARY_MD_FILE,
        pdf_path=EXECUTIVE_SUMMARY_PDF_FILE,
    )

    return {
        "technical_report": str(TECHNICAL_REPORT_MD_FILE),
        "executive_summary": str(EXECUTIVE_SUMMARY_MD_FILE),
        "architecture": str(ARCHITECTURE_MD_FILE),
        "methodology": str(METHODOLOGY_MD_FILE),
        "evidence_appendix": str(EVIDENCE_APPENDIX_MD_FILE),
        "figures": figures,
    }


def main() -> None:
    outputs = run_reporting()

    print("\nReporting artifacts generated.")
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()