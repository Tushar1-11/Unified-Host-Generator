from src.validator import (
    is_valid_domain,
    validate_domains,
)


def test_valid_domain():

    assert is_valid_domain(
        "ads.example.com"
    )


def test_invalid_ip():

    assert not is_valid_domain(
        "127.0.0.1"
    )


def test_invalid_localhost():

    assert not is_valid_domain(
        "localhost"
    )


def test_validate_collection():

    domains = {
        "ads.example.com",
        "127.0.0.1",
        "tracker.example.com",
    }

    result = validate_domains(domains)

    assert "ads.example.com" in result
    assert "tracker.example.com" in result
    assert "127.0.0.1" not in result