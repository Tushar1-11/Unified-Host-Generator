import argparse
import logging
import time
from pathlib import Path

from .config import (
    load_sources,
    load_domain_file,
    OUTPUT_DIR,
)

from .fetcher import fetch_source
from .parser import parse_blocklist
from .validator import (
    validate_domains,
    is_valid_domain,
)

from .filters import (
    apply_smart_whitelist,
)

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

    start_time = time.perf_counter()

    sources = load_sources()

    all_domains = []
    source_statistics = []

    raw_entries = 0
    successful_sources = 0

    # =========================================================
    # DOWNLOAD AND PARSE SOURCES
    # =========================================================

    for source in sources:

        name = source.get("name", "unknown")
        url = source.get("url")

        logger.info(
            "Downloading source: %s",
            name
        )

        if not url:
            logger.warning(
                "Skipping source without URL: %s",
                name
            )
            continue

        try:

            content = fetch_source(url)

            source_lines = len(
                content.splitlines()
            )

            parsed_domains = parse_blocklist(
                content
            )

            unique_source_domains = set(
                parsed_domains
            )

            all_domains.extend(
                parsed_domains
            )

            raw_entries += source_lines

            successful_sources += 1

            source_statistics.append({
                "name": name,
                "lines": source_lines,
                "parsed": len(parsed_domains),
                "unique": len(unique_source_domains),
            })

            logger.info(
                "%s: %d domains",
                name,
                len(unique_source_domains)
            )

        except Exception as error:

            logger.warning(
                "Failed to process %s: %s",
                name,
                error
            )

    # =========================================================
    # UNIQUE DOMAINS
    # =========================================================

    total_parsed = len(all_domains)

    unique_domains = set(all_domains)

    duplicates = (
        total_parsed -
        len(unique_domains)
    )

    # =========================================================
    # VALIDATION
    # =========================================================

    valid_domains = validate_domains(
        unique_domains
    )

    invalid_domains = (
        len(unique_domains) -
        len(valid_domains)
    )

    # =========================================================
    # LOAD CUSTOM FILTERS
    # =========================================================

    whitelist = load_domain_file(
        "whitelist.txt"
    )

    blacklist = load_domain_file(
        "blacklist.txt"
    )

    # Add custom blacklist
    valid_domains.update(
        blacklist
    )

    # =========================================================
    # APPLY WHITELIST
    # =========================================================

    before_whitelist = len(
        valid_domains
    )

    final_domains = apply_smart_whitelist(
        valid_domains,
        whitelist
    )

    whitelisted = (
        before_whitelist -
        len(final_domains)
    )

    # =========================================================
    # OUTPUT
    # =========================================================

    output_path = (
        Path(args.output)
        if args.output
        else OUTPUT_DIR / "hosts.txt"
    )

    # =========================================================
    # BACKUP
    # =========================================================

    if args.backup:

        backup_dir = (
            OUTPUT_DIR / "backups"
        )

        backup = backup_file(
            output_path,
            backup_dir
        )

        if backup:
            logger.info(
                "Backup created: %s",
                backup
            )

    # =========================================================
    # GENERATE HOSTS FILE
    # =========================================================

    write_hosts_file(
        final_domains,
        output_path,
        args.ip
    )

    logger.info(
        "Generated: %s",
        output_path
    )

    # =========================================================
    # COMPRESS
    # =========================================================

    if args.compress:

        compressed = compress_file(
            output_path
        )

        logger.info(
            "Compressed: %s",
            compressed
        )

    # =========================================================
    # PROCESSING TIME
    # =========================================================

    processing_time = (
        time.perf_counter() -
        start_time
    )

    # =========================================================
    # DISPLAY STATISTICS
    # =========================================================

    print_statistics(
        sources=successful_sources,
        raw_entries=raw_entries,
        parsed_domains=total_parsed,
        unique_domains=len(unique_domains),
        duplicates=duplicates,
        invalid_domains=invalid_domains,
        whitelisted=whitelisted,
        final_domains=len(final_domains),
        processing_time=processing_time,
        source_statistics=source_statistics,
    )

    print()
    print(
        f"Output: {output_path}"
    )
    print(
        "Generation complete."
    )


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

    # =========================================================
    # GENERATE COMMAND
    # =========================================================

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

    setup_logging(
        getattr(
            args,
            "verbose",
            False
        )
    )

    args.func(args)


if __name__ == "__main__":
    main()