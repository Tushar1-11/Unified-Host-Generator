from src.generator import (
    generate_hosts_content,
)


def test_hosts_generation():

    domains = {
        "ads.example.com",
        "tracker.example.com",
    }

    content = generate_hosts_content(
        domains
    )

    assert (
        "0.0.0.0 ads.example.com"
        in content
    )

    assert (
        "0.0.0.0 tracker.example.com"
        in content
    )