import polars as pl


ANOMALY_FEATURE_COLUMNS = [
    "total_requests",
    "unique_invoice_ids",
    "success_rate",
    "error_rate",
    "unique_tokens",
    "unique_user_agents",
    "requests_per_minute",
    "invoice_span",
    "sequential_access_ratio",
    "risk_score",
]


def build_anomaly_feature_frame(
    risk_scores: pl.DataFrame,
) -> pl.DataFrame:
    required = ["ip", *ANOMALY_FEATURE_COLUMNS]

    missing = [
        col
        for col in required
        if col not in risk_scores.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns for anomaly detection: {missing}"
        )

    return (
        risk_scores
        .select(required)
        .with_columns(
            [
                pl.col(col)
                .fill_null(0)
                .cast(pl.Float64)
                for col in ANOMALY_FEATURE_COLUMNS
            ]
        )
    )