import logging


def setup_logging(verbose=False):
    """Configure application logging."""

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )


def print_statistics(
    sources,
    raw_entries,
    valid_domains,
    duplicates,
    whitelisted,
    final_domains
):
    """Display generation statistics."""

    print()
    print("=" * 45)
    print(" Unified Hosts Generator")
    print("=" * 45)

    print(f"Sources processed : {sources}")
    print(f"Raw entries       : {raw_entries}")
    print(f"Valid domains     : {valid_domains}")
    print(f"Duplicates        : {duplicates}")
    print(f"Whitelisted       : {whitelisted}")
    print(f"Final domains     : {final_domains}")

    print("=" * 45)