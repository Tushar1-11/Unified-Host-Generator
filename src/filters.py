def apply_filters(domains, whitelist=None, blacklist=None):
    """
    Apply whitelist and blacklist.

    Blacklist adds domains.
    Whitelist removes domains.

    Returns:
        set[str]
    """

    result = set(domains)

    whitelist = whitelist or set()
    blacklist = blacklist or set()

    # Add custom blacklist
    result.update(blacklist)

    # Remove explicitly whitelisted domains
    result.difference_update(whitelist)

    return result


def is_whitelisted(domain, whitelist):
    """
    Check whether a domain is explicitly whitelisted.

    Also considers subdomains of a whitelisted domain.
    """

    domain = domain.lower()

    for allowed in whitelist:
        allowed = allowed.lower()

        if domain == allowed or domain.endswith("." + allowed):
            return True

    return False


def apply_smart_whitelist(domains, whitelist):
    """Remove whitelisted domains and their subdomains."""

    result = set()

    for domain in domains:
        if not is_whitelisted(domain, whitelist):
            result.add(domain)

    return result