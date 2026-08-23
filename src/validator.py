import re


DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


INVALID_DOMAINS = {
    "localhost",
    "local",
    "broadcasthost",
}


def is_valid_domain(domain):

    if not domain:
        return False

    domain = domain.strip().lower()

    if domain in INVALID_DOMAINS:
        return False

    # Reject IPv4 addresses
    if re.fullmatch(
        r"\d{1,3}(?:\.\d{1,3}){3}",
        domain
    ):
        return False

    return bool(
        DOMAIN_REGEX.match(domain)
    )


def validate_domains(domains):

    return {
        domain
        for domain in domains
        if is_valid_domain(domain)
    }