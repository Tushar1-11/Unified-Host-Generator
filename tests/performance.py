import time

from src.parser import parse_blocklist
from src.validator import validate_domains


def test_parser_performance():

    content = "\n".join(
        [
            f"0.0.0.0 domain{i}.example.com"
            for i in range(10000)
        ]
    )

    start = time.perf_counter()

    domains = parse_blocklist(
        content
    )

    valid = validate_domains(
        set(domains)
    )

    elapsed = (
        time.perf_counter() -
        start
    )

    assert len(valid) == 10000

    # Should comfortably process 10K
    # simple entries within this limit.
    assert elapsed < 5