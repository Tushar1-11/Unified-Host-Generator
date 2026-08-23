import re


def normalize_domain(domain):
    """Normalize a domain name."""

    domain = domain.strip().lower()

    if domain.startswith("http://"):
        domain = domain[7:]

    if domain.startswith("https://"):
        domain = domain[8:]

    if domain.startswith("www."):
        domain = domain[4:]

    domain = domain.split("/")[0]
    domain = domain.split(":")[0]
    domain = domain.rstrip(".")

    return domain


def extract_domain(line):
    """
    Extract a domain from common hosts/blocklist formats.

    Examples:
        0.0.0.0 example.com
        127.0.0.1 example.com
        example.com
    """

    line = line.strip()

    if not line or line.startswith("#"):
        return None

    # Remove inline comments
    if "#" in line:
        line = line.split("#", 1)[0].strip()

    parts = line.split()

    if not parts:
        return None

    if len(parts) >= 2:
        first = parts[0]

        if first in {
            "0.0.0.0",
            "127.0.0.1",
            "::",
            "::1",
            "localhost"
        }:
            domain = parts[1]
        else:
            domain = parts[0]
    else:
        domain = parts[0]

    return normalize_domain(domain)


def parse_blocklist(content):
    """
    Parse a blocklist.

    Returns:
        list[str]: parsed domains including duplicates
    """

    domains = []

    for line in content.splitlines():

        domain = extract_domain(line)

        if domain:
            domains.append(domain)

    return domains