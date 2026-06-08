import polars as pl

from src.parsing.uri_parser import (
    extract_uri_fields,
)


def test_uri_parser():

    df = pl.DataFrame(
        {
            "timestamp": [
                "2020-31-12T00:19"
            ],
            "status_code": [
                200
            ],
            "host": [
                "api.mercadolivre.com"
            ],
            "uri": [
                "/invoices/search?"
                "invoice_id=12345"
                "&site_id=MeliBR"
                "&authtoken=TOKEN123"
            ],
            "method": [
                "GET"
            ],
            "referer": [
                "https://mercadolivre.com"
            ],
            "user_agent": [
                "Mozilla"
            ],
            "source_ip": [
                "1.1.1.1"
            ],
        }
    )

    result = (
        extract_uri_fields(
            df.lazy()
        )
        .collect()
    )

    assert result["invoice_id"][0] == 12345
    assert result["site_id"][0] == "MeliBR"
    assert result["auth_token"][0] == "TOKEN123"

    assert result["timestamp"][0].year == 2020
    assert result["timestamp"][0].month == 12
    assert result["timestamp"][0].day == 31