from pathlib import Path

import polars as pl


def detect_idor_findings(
    ip_features: pl.DataFrame,
    min_unique_invoice_ids: int = 750,
    min_sequential_access_ratio: float = 0.35,
    min_total_requests: int = 1000,
) -> pl.DataFrame:
    return (
        ip_features
        .with_columns(
            [
                (
                    (pl.col("unique_invoice_ids") >= min_unique_invoice_ids)
                    &
                    (pl.col("sequential_access_ratio") >= min_sequential_access_ratio)
                    &
                    (pl.col("total_requests") >= min_total_requests)
                ).alias("is_idor_suspect"),

                pl.when(
                    pl.col("sequential_access_ratio") >= 0.60
                )
                .then(pl.lit("critical"))
                .when(
                    pl.col("sequential_access_ratio") >= 0.40
                )
                .then(pl.lit("high"))
                .when(
                    pl.col("sequential_access_ratio") >= 0.25
                )
                .then(pl.lit("medium"))
                .otherwise(pl.lit("low"))
                .alias("idor_severity"),

                pl.concat_str(
                    [
                        pl.lit("Sequential invoice enumeration pattern. "),
                        pl.lit("unique_invoice_ids="),
                        pl.col("unique_invoice_ids").cast(pl.Utf8),
                        pl.lit(", total_requests="),
                        pl.col("total_requests").cast(pl.Utf8),
                        pl.lit(", sequential_access_ratio="),
                        pl.col("sequential_access_ratio").round(4).cast(pl.Utf8),
                    ]
                ).alias("idor_evidence"),
            ]
        )
        .filter(pl.col("is_idor_suspect"))
        .select(
            [
                "ip",
                "total_requests",
                "unique_invoice_ids",
                "successful_requests",
                "failed_requests",
                "success_rate",
                "error_rate",
                "unique_tokens",
                "unique_user_agents",
                "first_seen",
                "last_seen",
                "active_minutes",
                "requests_per_minute",
                "min_invoice_id",
                "max_invoice_id",
                "invoice_span",
                "sequential_access_ratio",
                "is_idor_suspect",
                "idor_severity",
                "idor_evidence",
            ]
        )
        .sort(
            [
                "idor_severity",
                "sequential_access_ratio",
                "unique_invoice_ids",
            ],
            descending=[False, True, True],
        )
    )


def save_idor_findings(
    findings: pl.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    findings.write_parquet(output_file)