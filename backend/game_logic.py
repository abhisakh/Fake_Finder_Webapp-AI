import random
from typing import List, Tuple

def parse_facts(fact_string: str) -> List[Tuple[str, bool]]:
    """
    Parses the pipe-separated string from the Gemini API into a list of
    fact-boolean tuples.

    Args:
        fact_string: The output string from the generate_facts function.

    Returns:
        A list of tuples: [(sentence, is_true), ...].
    """
    result = []
    items = fact_string.strip().split("|")

    for item in items:
        parts = item.split("@")
        if len(parts) == 2:
            try:
                # Extract sentence and boolean, stripping formatting
                sentence = parts[0].strip().lstrip('(').strip()
                boolean_str = parts[1].strip().rstrip(')').strip()
                is_true = boolean_str.lower() == "true"
                result.append((sentence, is_true))
            except Exception:
                # Skip malformed items
                continue

    return result


def shuffle_facts(facts: List[Tuple[str, bool]]) -> List[Tuple[str, bool]]:
    """
    Shuffles the facts list and returns a copy.
    """
    shuffled = list(facts)
    random.shuffle(shuffled)
    return shuffled


def get_correct_index(facts: List[Tuple[str, bool]]) -> int:
    """
    Finds the 0-based index of the fake (False) statement in the list.
    """
    for index, (_, is_true) in enumerate(facts):
        if not is_true:
            return index
    return -1 # Should not happen if AI output is correct
