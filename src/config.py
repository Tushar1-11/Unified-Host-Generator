import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"


def load_sources():
    """Load enabled blocklist sources from sources.json."""

    config_file = CONFIG_DIR / "sources.json"

    with open(config_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        source
        for source in data.get("sources", [])
        if source.get("enabled", True)
    ]


def load_domain_file(filename):
    """Load domains from a text file."""

    path = CONFIG_DIR / filename

    if not path.exists():
        return set()

    domains = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            domains.add(line.lower())

    return domains