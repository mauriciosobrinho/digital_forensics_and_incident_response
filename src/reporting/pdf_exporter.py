from pathlib import Path


def export_markdown_to_pdf(
    markdown_path: Path,
    pdf_path: Path,
) -> None:
    """
    Best-effort PDF exporter.

    On Windows, WeasyPrint may require external GTK/Pango libraries.
    If those libraries are not available, the pipeline must not fail.
    In that case, a marker file is created and the DOCX/MD reports remain
    the authoritative deliverables.
    """

    try:
        import markdown
        from weasyprint import HTML

        html = markdown.markdown(
            markdown_path.read_text(encoding="utf-8"),
            extensions=[
                "tables",
                "fenced_code",
            ],
        )

        HTML(
            string=html,
            base_url=str(markdown_path.parent),
        ).write_pdf(str(pdf_path))

    except Exception as exc:
        marker_path = pdf_path.with_suffix(
            pdf_path.suffix + ".not_generated.txt"
        )

        marker_path.write_text(
            (
                "PDF was not generated automatically.\n"
                "Reason: WeasyPrint or one of its native dependencies "
                "is not available in this environment.\n\n"
                f"Source markdown: {markdown_path}\n"
                f"Expected PDF: {pdf_path}\n"
                f"Error: {repr(exc)}\n\n"
                "Export the DOCX or Markdown manually to PDF using "
                "Word, LibreOffice or another document renderer.\n"
            ),
            encoding="utf-8",
        )

        print(
            f"PDF export skipped: {marker_path}"
        )