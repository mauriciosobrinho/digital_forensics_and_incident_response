from pathlib import Path
import json

import polars as pl


def build_attack_timeline(
    parsed_events: pl.DataFrame,
    suspicious_ips: pl.DataFrame,
    top_n: int = 20,
) -> dict:
    top_ips = (
        suspicious_ips
        .sort("risk_score", descending=True)
        .select("ip")
        .head(top_n)
        .to_series()
        .to_list()
    )

    if not top_ips:
        return {
            "timeline_type": "attack_timeline",
            "top_ips": [],
            "events": [],
            "summary": {
                "total_attack_events": 0,
                "first_seen": None,
                "last_seen": None,
            },
        }

    attack_events = (
        parsed_events
        .filter(
            pl.col("source_ip").is_in(top_ips)
        )
        .with_columns(
            [
                pl.col("timestamp").cast(pl.Utf8).alias("timestamp"),
            ]
        )
    )

    summary_df = attack_events.select(
        [
            pl.len().alias("total_attack_events"),
            pl.col("timestamp").min().alias("first_seen"),
            pl.col("timestamp").max().alias("last_seen"),
            pl.col("source_ip").n_unique().alias("unique_attack_ips"),
            pl.col("invoice_id").n_unique().alias("unique_invoices_accessed"),
            pl.col("auth_token").n_unique().alias("unique_tokens_seen"),
        ]
    )

    summary = summary_df.to_dicts()[0]

    hourly = (
        attack_events
        .with_columns(
            pl.col("timestamp")
            .str.slice(0, 13)
            .alias("hour_bucket")
        )
        .group_by("hour_bucket")
        .agg(
            [
                pl.len().alias("requests"),
                pl.col("source_ip").n_unique().alias("unique_ips"),
                pl.col("invoice_id").n_unique().alias("unique_invoice_ids"),
            ]
        )
        .sort("hour_bucket")
    )

    by_ip = (
        attack_events
        .group_by("source_ip")
        .agg(
            [
                pl.len().alias("requests"),
                pl.col("invoice_id").n_unique().alias("unique_invoice_ids"),
                pl.col("timestamp").min().alias("first_seen"),
                pl.col("timestamp").max().alias("last_seen"),
            ]
        )
        .sort("requests", descending=True)
    )

    return {
        "timeline_type": "attack_timeline",
        "top_ips": top_ips,
        "summary": summary,
        "hourly_timeline": hourly.to_dicts(),
        "attacker_timelines": by_ip.to_dicts(),
    }


def save_attack_timeline(
    timeline: dict,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            timeline,
            f,
            indent=2,
            ensure_ascii=False,
        )