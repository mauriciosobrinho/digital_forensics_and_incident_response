from pathlib import Path

import polars as pl

from src.detection.anomaly_features import (
    build_anomaly_feature_frame,
)

from src.detection.isolation_forest import (
    run_isolation_forest,
)


def detect_anomalies(
    risk_scores: pl.DataFrame,
    contamination: float = 0.03,
) -> pl.DataFrame:
    anomaly_features = build_anomaly_feature_frame(
        risk_scores
    )

    anomaly_scores = run_isolation_forest(
        anomaly_features,
        contamination=contamination,
    )

    return (
        risk_scores
        .join(
            anomaly_scores.select(
                [
                    "ip",
                    "isolation_forest_label",
                    "isolation_forest_decision_score",
                    "anomaly_score",
                    "is_anomalous",
                ]
            ),
            on="ip",
            how="left",
        )
        .with_columns(
            [
                pl.col("is_anomalous")
                .fill_null(False),

                pl.col("anomaly_score")
                .fill_null(0.0),

                pl.col("isolation_forest_label")
                .fill_null(1),

                pl.col("isolation_forest_decision_score")
                .fill_null(0.0),
            ]
        )
        .with_columns(
            pl.when(
                pl.col("anomaly_score") >= 85
            )
            .then(pl.lit("critical"))
            .when(
                pl.col("anomaly_score") >= 70
            )
            .then(pl.lit("high"))
            .when(
                pl.col("anomaly_score") >= 50
            )
            .then(pl.lit("medium"))
            .otherwise(pl.lit("low"))
            .alias("anomaly_level")
        )
        .sort(
            "anomaly_score",
            descending=True,
        )
    )


def build_anomalous_ips(
    anomaly_scores: pl.DataFrame,
) -> pl.DataFrame:
    return (
        anomaly_scores
        .filter(
            pl.col("is_anomalous")
        )
        .sort(
            "anomaly_score",
            descending=True,
        )
    )


def save_anomaly_scores(
    anomaly_scores: pl.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    anomaly_scores.write_parquet(
        output_file
    )


def save_anomalous_ips(
    anomalous_ips: pl.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    anomalous_ips.write_parquet(
        output_file
    )