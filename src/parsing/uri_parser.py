import polars as pl


def extract_uri_fields(
    logs: pl.LazyFrame,
) -> pl.LazyFrame:

    return logs.with_columns(
        [
            pl.col("uri")
            .str.extract(
                r"invoice_id=(\d+)",
                1,
            )
            .cast(pl.Int64)
            .alias("invoice_id"),

            pl.col("uri")
            .str.extract(
                r"site_id=([^&]+)",
                1,
            )
            .alias("site_id"),

            pl.col("uri")
            .str.extract(
                r"authtoken=([^&]+)",
                1,
            )
            .alias("auth_token"),
        ]
    )


def persist_parsed_events(
    events: pl.LazyFrame,
    output_file,
) -> None:

    (
        events
        .collect(streaming=True)
        .write_parquet(output_file)
    )
