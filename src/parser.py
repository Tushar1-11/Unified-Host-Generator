import re


DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"\.)+"
    r"[a-zA-Z]{2,63}\.?$"
)


def normalize_domain(domain):
    """Normalize a domain name."""

    domain = domain.strip().lower()

    # Remove protocol
    if domain.startswith("http://"):
        domain = domain[7:]

    if domain.startswith("https://"):
        domain = domain[8:]

    # Remove www.
    if domain.startswith("www."):
        domain = domain[4:]

    # Remove path
    domain = domain.split("/")[0]

    # Remove port
    domain = domain.split(":")[0]

    # Remove trailing dot
    domain = domain.rstrip(".")

    return domain


def extract_domain(line):
    """
    Extract a domain from a blocklist line.

    Supports:
        0.0.0.0 example.com
        127.0.0.1 example.com
        example.com
    """

    line = line.strip()

    # Empty/comment line
    if not line or line.startswith("#"):
        return None

    # Remove inline comments
    if "#" in line:
        line = line.split("#", 1)[0].strip()

    parts = line.split()

    if not parts:
        return None

    # Hosts format:
    # 0.0.0.0 example.com
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

    domain = normalize_domain(domain)

    if not domain:
        return None

    return domain


def parse_blocklist(content):
    """
    Parse complete blocklist content.

    Returns:
        set[str]: unique domains
    """

    domains = set()

    for line in content.splitlines():
        domain = extract_domain(line)

        if domain:
            domains.add(domain)

    return domains