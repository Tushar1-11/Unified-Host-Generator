import logging


def setup_logging(verbose=False):

    level = (
        logging.DEBUG
        if verbose
        else logging.INFO
    )

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )


def print_statistics(
    sources,
    raw_entries,
    parsed_domains,
    unique_domains,
    duplicates,
    invalid_domains,
    whitelisted,
    final_domains,
    processing_time,
    source_statistics,
):

    print()

    print("=" * 55)
    print(" Unified Hosts Generator")
    print("=" * 55)

    print(
        f"Sources processed : {sources}"
    )

    print(
        f"Raw entries       : {raw_entries}"
    )

    print(
        f"Parsed domains    : {parsed_domains}"
    )

    print(
        f"Unique domains    : {unique_domains}"
    )

    print(
        f"Duplicates        : {duplicates}"
    )

    print(
        f"Invalid domains   : {invalid_domains}"
    )

    print(
        f"Whitelisted       : {whitelisted}"
    )

    print(
        f"Final domains     : {final_domains}"
    )

    print(
        f"Processing time   : "
        f"{processing_time:.2f} seconds"
    )

    print("=" * 55)

    print()

    print("Source Statistics")
    print("-" * 55)

    for source in source_statistics:

        print(
            f"{source['name']}: "
            f"{source['unique']} unique domains "
            f"({source['parsed']} parsed)"
        )

    print("-" * 55)