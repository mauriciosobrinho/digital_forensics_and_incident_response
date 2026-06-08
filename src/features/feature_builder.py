from pathlib import Path

import numpy as np
import polars as pl


def build_ip_features(
    parsed_events: pl.LazyFrame,
) -> pl.DataFrame:

    agg = (
        parsed_events
        .group_by("source_ip")
        .agg(
            [
                pl.len().alias("total_requests"),

                pl.col("invoice_id")
                .n_unique()
                .alias("unique_invoice_ids"),

                pl.col("invoice_id")
                .drop_nulls()
                .alias("invoice_ids_list"),

                pl.col("auth_token")
                .n_unique()
                .alias("unique_tokens"),

                pl.col("user_agent")
                .n_unique()
                .alias("unique_user_agents"),

                (pl.col("status_code") < 400)
                .sum()
                .alias("successful_requests"),

                (pl.col("status_code") >= 400)
                .sum()
                .alias("failed_requests"),

                pl.col("timestamp")
                .min()
                .alias("first_seen"),

                pl.col("timestamp")
                .max()
                .alias("last_seen"),

                pl.col("invoice_id")
                .min()
                .alias("min_invoice_id"),

                pl.col("invoice_id")
                .max()
                .alias("max_invoice_id"),
            ]
        )
    )

    features = agg.collect()

    def sequential_ratio(values):

        if values is None:
            return 0.0

        ids = sorted(
            {
                int(v)
                for v in values
                if v is not None
            }
        )

        if len(ids) < 2:
            return 0.0

        diffs = np.diff(ids)

        if len(diffs) == 0:
            return 0.0

        return float(
            (diffs == 1).sum()
        ) / float(len(diffs))

    features = (
        features
        .with_columns(
            [
                (
                    pl.col("successful_requests")
                    / pl.col("total_requests")
                )
                .alias("success_rate"),

                (
                    pl.col("failed_requests")
                    / pl.col("total_requests")
                )
                .alias("error_rate"),

                (
                    (
                        pl.col("last_seen")
                        -
                        pl.col("first_seen")
                    )
                    .dt.total_seconds()
                    / 60
                )
                .alias("active_minutes"),

                (
                    pl.col("max_invoice_id")
                    -
                    pl.col("min_invoice_id")
                )
                .alias("invoice_span"),
            ]
        )
        .with_columns(
            [
                pl.when(
                    pl.col("active_minutes") > 0
                )
                .then(
                    pl.col("total_requests")
                    /
                    pl.col("active_minutes")
                )
                .otherwise(
                    pl.col("total_requests")
                )
                .alias("requests_per_minute"),

                pl.col("invoice_ids_list")
                .map_elements(
                    sequential_ratio,
                    return_dtype=pl.Float64,
                )
                .alias("sequential_access_ratio"),
            ]
        )
        .rename(
            {
                "source_ip": "ip",
            }
        )
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
            ]
        )
    )

    return features


def save_ip_features(
    features: pl.DataFrame,
    output_file: Path,
) -> None:
    features.write_parquet(output_file)