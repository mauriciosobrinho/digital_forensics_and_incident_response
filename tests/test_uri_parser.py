import polars as pl

from src.parsing.uri_parser import (
    extract_uri_fields,
)


def test_uri_parser():

    df = pl.DataFrame(
        {
            "uri": [
                "/invoices/search?"
                "invoice_id=12345"
                "&site_id=MeliBR"
                "&authtoken=TOKEN123"
            ]
        }
    )

    result = (
        extract_uri_fields(
            df.lazy()
        )
        .collect()
    )

    assert (
        result["invoice_id"][0]
        == 12345
    )

    assert (
        result["site_id"][0]
        == "MeliBR"
    )

    assert (
        result["auth_token"][0]
        == "TOKEN123"
    )
