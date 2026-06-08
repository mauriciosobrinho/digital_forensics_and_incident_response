from pathlib import Path
from urllib.parse import parse_qs, urlparse

import polars as pl


def extract_uri_fields(
    logs: pl.LazyFrame,
) -> pl.LazyFrame:
    """
    Parse raw events and normalize fields required by DFIR analysis.

    IMPORTANT:
    The challenge dataset stores timestamps as:

        %Y-%d-%mT%H:%M

    Example:

        2020-31-12T00:19

    which means:

        2020-12-31T00:19

    We normalize this immediately so every downstream
    component works with a true Datetime column.
    """

    def extract_invoice_id(uri: str):
        try:
            return int(
                parse_qs(
                    urlparse(uri).query
                ).get("invoice_id", [None])[0]
            )
        except Exception:
            return None

    def extract_site_id(uri: str):
        try:
            return (
                parse_qs(
                    urlparse(uri).query
                ).get("site_id", [None])[0]
            )
        except Exception:
            return None

    def extract_token(uri: str):
        try:
            return (
                parse_qs(
                    urlparse(uri).query
                ).get("authtoken", [None])[0]
            )
        except Exception:
            return None

    return (
        logs
        .with_columns(
            [
                pl.col("timestamp")
                .str.strptime(
                    pl.Datetime,
                    format="%Y-%d-%mT%H:%M",
                    strict=False,
                )
                .alias("timestamp"),

                pl.col("status_code")
                .cast(pl.Int32)
                .alias("status_code"),

                pl.col("user_agent")
                .alias("user_agent"),
            ]
        )
        .with_columns(
            [
                pl.col("uri")
                .map_elements(
                    extract_invoice_id,
                    return_dtype=pl.Int64,
                )
                .alias("invoice_id"),

                pl.col("uri")
                .map_elements(
                    extract_site_id,
                    return_dtype=pl.Utf8,
                )
                .alias("site_id"),

                pl.col("uri")
                .map_elements(
                    extract_token,
                    return_dtype=pl.Utf8,
                )
                .alias("auth_token"),
            ]
        )
        .select(
            [
                "timestamp",
                "status_code",
                "host",
                "method",
                "source_ip",
                "user_agent",
                "invoice_id",
                "site_id",
                "auth_token",
            ]
        )
    )


def persist_parsed_events(
    events: pl.LazyFrame,
    output_file: Path,
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    events.sink_parquet(
        output_file
    )