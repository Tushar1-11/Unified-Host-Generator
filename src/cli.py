import argparse
import logging
from pathlib import Path

from .config import (
    load_sources,
    load_domain_file,
    OUTPUT_DIR,
)

from .fetcher import fetch_source
from .parser import parse_blocklist
from .validator import validate_domains
from .filters import apply_smart_whitelist
from .generator import (
    write_hosts_file,
    compress_file,
    backup_file,
)
from .utils import (
    setup_logging,
    print_statistics,
)


logger = logging.getLogger(__name__)


def generate_hosts(args):
    """Main generation workflow."""

    sources = load_sources()

    all_domains = set()
    raw_entries = 0
    successful_sources = 0

    for source in sources:

        name = source.get("name", "unknown")
        url = source.get("url")

        logger.info("Downloading source: %s", name)

        if not url:
            logger.warning(
                "Skipping source without URL: %s",
                name
            )
            continue

        try:
            content = fetch_source(url)

            raw_entries += len(
                content.splitlines()
            )

            domains = parse_blocklist(content)

            all_domains.update(domains)

            successful_sources += 1

            logger.info(
                "%s: %d domains",
                name,
                len(domains)
            )

        except Exception as error:
            logger.warning(
                "Failed to process %s: %s",
                name,
                error
            )

    # Validate
    valid_domains = validate_domains(all_domains)

    duplicates = len(all_domains) - len(valid_domains)

    # Load filters
    whitelist = load_domain_file(
        "whitelist.txt"
    )

    blacklist = load_domain_file(
        "blacklist.txt"
    )

    # Add blacklist
    valid_domains.update(blacklist)

    # Apply whitelist including subdomains
    before_whitelist = len(valid_domains)

    final_domains = apply_smart_whitelist(
        valid_domains,
        whitelist
    )

    whitelisted = (
        before_whitelist -
        len(final_domains)
    )

    # Output
    output_path = (
        Path(args.output)
        if args.output
        else OUTPUT_DIR / "hosts.txt"
    )

    # Backup
    if args.backup:
        backup_dir = OUTPUT_DIR / "backups"

        backup = backup_file(
            output_path,
            backup_dir
        )

        if backup:
            logger.info(
                "Backup created: %s",
                backup
            )

    # Generate
    write_hosts_file(
        final_domains,
        output_path,
        args.ip
    )

    logger.info(
        "Generated: %s",
        output_path
    )

    # Compression
    if args.compress:
        compressed = compress_file(
            output_path
        )

        logger.info(
            "Compressed: %s",
            compressed
        )

    print_statistics(
        successful_sources,
        raw_entries,
        len(valid_domains),
        duplicates,
        whitelisted,
        len(final_domains)
    )

    print()
    print(f"Output: {output_path}")
    print("Generation complete.")


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Unified Hosts File Generator "
            "for DNS and content blocking"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate hosts file"
    )

    generate_parser.add_argument(
        "--output",
        help="Output hosts file path"
    )

    generate_parser.add_argument(
        "--ip",
        default="0.0.0.0",
        help="IP address used for blocking"
    )

    generate_parser.add_argument(
        "--compress",
        action="store_true",
        help="Create gzip compressed output"
    )

    generate_parser.add_argument(
        "--backup",
        action="store_true",
        help="Backup existing output file"
    )

    generate_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    generate_parser.set_defaults(
        func=generate_hosts
    )

    args = parser.parse_args()

    if hasattr(args, "verbose"):
        setup_logging(args.verbose)
    else:
        setup_logging(False)

    args.func(args)


if __name__ == "__main__":
    main()