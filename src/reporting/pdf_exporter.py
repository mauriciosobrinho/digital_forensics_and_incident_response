from pathlib import Path


def export_markdown_to_pdf(
    *,
    markdown_path: Path,
    pdf_path: Path,
) -> None:
    try:
        import markdown
        from weasyprint import HTML
    except ImportError:
        return

    html = markdown.markdown(
        markdown_path.read_text(encoding="utf-8"),
        extensions=[
            "tables",
            "fenced_code",
        ],
    )

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    HTML(
        string=html,
        base_url=str(markdown_path.parent),
    ).write_pdf(
        str(pdf_path)
    )