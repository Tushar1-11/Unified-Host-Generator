from src.filters import (
    apply_filters,
    apply_smart_whitelist,
)


def test_blacklist():

    domains = {
        "ads.example.com"
    }

    blacklist = {
        "tracker.example.com"
    }

    result = apply_filters(
        domains,
        blacklist=blacklist
    )

    assert "ads.example.com" in result
    assert "tracker.example.com" in result


def test_whitelist():

    domains = {
        "ads.example.com",
        "tracker.example.com",
    }

    whitelist = {
        "example.com"
    }

    result = apply_smart_whitelist(
        domains,
        whitelist
    )

    assert len(result) == 0