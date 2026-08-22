from unittest.mock import patch

from src.fetcher import fetch_source


@patch("src.fetcher.requests.get")
def test_fetch_source(mock_get):

    mock_get.return_value.text = (
        "0.0.0.0 ads.example.com"
    )

    mock_get.return_value.raise_for_status.return_value = None

    result = fetch_source(
        "https://example.com/list.txt"
    )

    assert (
        result ==
        "0.0.0.0 ads.example.com"
    )