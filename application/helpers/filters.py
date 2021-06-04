from typing import List


def filter_messages(source: str, to_match: List[str]) -> bool:
    """Check if string contain any of forbidden wordlist

    Args:
        source (str): string to compare
        to_match (List[str]): Forbidden words list

    Returns:
        bool: True if it contain forbidden words
    """
    src = source.lower().split(' ')

    for word in to_match:
        if word in set(src):
            return False

    return True
