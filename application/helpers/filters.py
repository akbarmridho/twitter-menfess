from typing import List


def filter_messages(source: str, to_match: List[str]) -> bool:
    src = source.lower()

    for keyword in to_match:
        if keyword.lower() in src:
            return True

    return False
