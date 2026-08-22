import requests


def fetch_source(url, timeout=30):
    """
    Download a blocklist from a URL.

    Returns:
        str: downloaded content

    Raises:
        requests.RequestException: if download fails
    """

    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": "UnifiedHostsGenerator/1.0"
        }
    )

    response.raise_for_status()

    return response.text