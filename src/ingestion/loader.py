from pathlib import Path

import polars as pl


def load_logs(file_path: Path) -> pl.LazyFrame:

    return (
        pl.scan_csv(file_path)
        .rename(
            {
                "http_staus": "status_code",
                "http_host": "host",
                "http_uri": "uri",
                "http_method": "method",
                "http_referer": "referer",
                "http_user_agent": "user_agent",
            }
        )
    )
