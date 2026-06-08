from pathlib import Path

import polars as pl


def build_risk_scores(
    ip_features: pl.DataFrame,
    bot_signals: pl.DataFrame,
    idor_findings: pl.DataFrame,
) -> pl.DataFrame:
    max_requests = max(
        ip_features["total_requests"].max(),
        1,
    )

    max_unique_invoices = max(
        ip_features["unique_invoice_ids"].max(),
        1,
    )

    max_rpm = max(
        ip_features["requests_per_minute"].max(),
        1e-9,
    )

    idor_flags = (
        idor_findings
        .select(
            [
                "ip",
                "is_idor_suspect",
                "idor_severity",
                "idor_evidence",
            ]
        )
        if idor_findings.height > 0
        else pl.DataFrame(
            {
                "ip": [],
                "is_idor_suspect": [],
                "idor_severity": [],
                "idor_evidence": [],
            },
            schema={
                "ip": pl.Utf8,
                "is_idor_suspect": pl.Boolean,
                "idor_severity": pl.Utf8,
                "idor_evidence": pl.Utf8,
            },
        )
    )

    return (
        ip_features
        .join(
            bot_signals,
            on="ip",
            how="left",
        )
        .join(
            idor_flags,
            on="ip",
            how="left",
        )
        .with_columns(
            [
                pl.col("is_idor_suspect")
                .fill_null(False),

                pl.col("idor_severity")
                .fill_null("none"),

                pl.col("idor_evidence")
                .fill_null("No IDOR evidence above configured thresholds."),

                pl.col("bot_likelihood_score")
                .fill_null(0.0),

                pl.col("is_likely_bot")
                .fill_null(False),
            ]
        )
        .with_columns(
            [
                (
                    pl.col("total_requests") / max_requests
                ).clip(0, 1).alias("risk_request_volume_component"),

                (
                    pl.col("unique_invoice_ids") / max_unique_invoices
                ).clip(0, 1).alias("risk_invoice_diversity_component"),

                (
                    pl.col("requests_per_minute") / max_rpm
                ).clip(0, 1).alias("risk_velocity_component"),

                pl.col("sequential_access_ratio")
                .clip(0, 1)
                .alias("risk_sequential_component"),

                pl.col("success_rate")
                .clip(0, 1)
                .alias("risk_success_component"),
            ]
        )
        .with_columns(
            (
                (
                    pl.col("risk_sequential_component") * 35
                    + pl.col("risk_invoice_diversity_component") * 25
                    + pl.col("risk_request_volume_component") * 20
                    + pl.col("risk_velocity_component") * 10
                    + pl.col("risk_success_component") * 10
                )
            ).alias("risk_score")
        )
        .with_columns(
            pl.when(
                pl.col("risk_score") >= 80
            )
            .then(pl.lit("critical"))
            .when(
                pl.col("risk_score") >= 60
            )
            .then(pl.lit("high"))
            .when(
                pl.col("risk_score") >= 40
            )
            .then(pl.lit("medium"))
            .otherwise(pl.lit("low"))
            .alias("risk_level")
        )
        .sort(
            "risk_score",
            descending=True,
        )
    )


def build_suspicious_ips(
    risk_scores: pl.DataFrame,
    min_risk_score: float = 60.0,
) -> pl.DataFrame:
    return (
        risk_scores
        .filter(
            (pl.col("risk_score") >= min_risk_score)
            |
            (pl.col("is_idor_suspect"))
            |
            (pl.col("is_likely_bot"))
        )
        .sort(
            "risk_score",
            descending=True,
        )
    )


def save_risk_scores(
    risk_scores: pl.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    risk_scores.write_parquet(output_file)


def save_suspicious_ips(
    suspicious_ips: pl.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    suspicious_ips.write_parquet(output_file)