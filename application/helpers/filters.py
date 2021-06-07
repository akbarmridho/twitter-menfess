from typing import List


def filter_messages(source: str, to_match: List[str]) -> bool:
    """Check if string contain any of forbidden wordlist

    Args:
        source (str): string to compare
        to_match (List[str]): Forbidden words list

    Returns:
        bool: True if it contain forbidden words
    """
    lines = source.lower().splitlines()

    to_filters = []

    for line in lines:
        to_filters.extend(line.split(' '))

    for word in to_match:
        if word in set(to_filters):
            return False

    return True
