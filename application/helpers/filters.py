from typing import List


def filter_messages(source: str, to_match: List[str]) -> bool:
    src = source.lower()

    res = set(to_match).intersection(set(src.split()))

    return len(res) == 0
