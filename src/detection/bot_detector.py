import polars as pl


def detect_bot_signals(
    ip_features: pl.DataFrame,
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

    return (
        ip_features
        .with_columns(
            [
                (
                    pl.col("total_requests") / max_requests
                ).clip(0, 1).alias("request_volume_score"),

                (
                    pl.col("unique_invoice_ids") / max_unique_invoices
                ).clip(0, 1).alias("invoice_diversity_score"),

                (
                    pl.col("requests_per_minute") / max_rpm
                ).clip(0, 1).alias("velocity_score"),

                (
                    1 / pl.col("unique_user_agents").clip(1, None)
                ).alias("user_agent_consistency_score"),
            ]
        )
        .with_columns(
            (
                (
                    pl.col("request_volume_score") * 0.30
                    + pl.col("invoice_diversity_score") * 0.30
                    + pl.col("velocity_score") * 0.20
                    + pl.col("sequential_access_ratio") * 0.15
                    + pl.col("user_agent_consistency_score") * 0.05
                ) * 100
            ).alias("bot_likelihood_score")
        )
        .with_columns(
            (
                pl.col("bot_likelihood_score") >= 65
            ).alias("is_likely_bot")
        )
        .select(
            [
                "ip",
                "request_volume_score",
                "invoice_diversity_score",
                "velocity_score",
                "user_agent_consistency_score",
                "bot_likelihood_score",
                "is_likely_bot",
            ]
        )
    )