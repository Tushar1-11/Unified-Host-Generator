from pathlib import Path
from datetime import datetime
import gzip
import shutil


def generate_hosts_content(domains, ip="0.0.0.0"):
    """
    Generate hosts-file content from domains.
    """

    lines = [
        "# Unified Hosts File Generator",
        f"# Generated: {datetime.now().isoformat()}",
        f"# Domains: {len(domains)}",
        "",
    ]

    for domain in sorted(domains):
        lines.append(f"{ip} {domain}")

    lines.append("")

    return "\n".join(lines)


def write_hosts_file(domains, output_path, ip="0.0.0.0"):
    """Write hosts file to disk."""

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    content = generate_hosts_content(domains, ip)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

    return output_path


def compress_file(input_path, output_path=None):
    """Compress a file using gzip."""

    input_path = Path(input_path)

    if output_path is None:
        output_path = Path(str(input_path) + ".gz")
    else:
        output_path = Path(output_path)

    with open(input_path, "rb") as source:
        with gzip.open(output_path, "wb") as destination:
            shutil.copyfileobj(source, destination)

    return output_path


def backup_file(file_path, backup_dir):
    """Create a timestamped backup."""

    file_path = Path(file_path)
    backup_dir = Path(backup_dir)

    if not file_path.exists():
        return None

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = (
        backup_dir /
        f"{file_path.stem}_{timestamp}{file_path.suffix}"
    )

    shutil.copy2(file_path, backup_path)

    return backup_path