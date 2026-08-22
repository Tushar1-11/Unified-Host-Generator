from src.parser import (
    extract_domain,
    parse_blocklist,
)


def test_extract_hosts_format():
    assert (
        extract_domain(
            "0.0.0.0 ads.example.com"
        )
        == "ads.example.com"
    )


def test_extract_plain_domain():
    assert (
        extract_domain(
            "tracker.example.com"
        )
        == "tracker.example.com"
    )


def test_ignore_comment():
    assert (
        extract_domain(
            "# this is a comment"
        )
        is None
    )


def test_parse_duplicates():

    content = """
    0.0.0.0 ads.example.com
    0.0.0.0 ads.example.com
    tracker.example.com
    """

    domains = parse_blocklist(content)

    assert len(domains) == 2