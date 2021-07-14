from typing import List


def split_message(source: str, limit: int = 280) -> List[str]:
    """Split single string into list of string limited by their length.

    If list have more than one element, every element except the last
    will contain ' cont.' string.

    This function will truncate by words.

    Args:
        source (str): [description]
        limit (int, optional): [description]. Defaults to 280.

    Returns:
        List[str]: [description]
    """
    source = source.strip()

    if len(source) < limit:
        return [source]

    split_index = source[:limit-6].rfind(' ')

    if split_index == -1 or split_index == 0:
        split_index = limit-6

    return [source[:split_index] + ' cont.', *split_message(source[split_index:], limit)]


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
