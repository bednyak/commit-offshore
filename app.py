from typing import List
from collections import Counter

# ─────────────────────────────────────────────────────────
# Task 1 – Maximum number investor meetings that can be held
# ─────────────────────────────────────────────────────────
def count_meetings(first_days_available: List[int], last_days_available: List[int]) -> int:
    # ── 1. Basic shape check ────────────────────────────────────────────────
    first_days_elements_amount = len(first_days_available)
    last_days_elements_amount = len(last_days_available)
    if first_days_elements_amount != last_days_elements_amount:
        raise ValueError("first and last must be the same length")
    if not (1 <= first_days_elements_amount <= 100_000):
        raise ValueError(f"n (= {first_days_elements_amount}) must be between 1 and 100 000")

    # ── 2. Per-element range & ordering checks ──────────────────────────────
    for i, (f, l) in enumerate(zip(first_days_available, last_days_available)):
        if not (1 <= f <= 100_000):
            raise ValueError(f"firstDay[{i}] = {f} is out of [1, 100 000]")
        if not (1 <= l <= 100_000):
            raise ValueError(f"lastDay[{i}]  = {l} is out of [1, 100 000]")
        if f > l:
            raise ValueError(
                f"firstDay[{i}] (= {f}) must be ≤ lastDay[{i}] (= {l})"
            )

    # ── 3. Greedy scheduling ─────────────────────────
    slots = sorted(zip(first_days_available, last_days_available), key=lambda p: (p[1], p[0]))  # (start, end)

    next_free = float("-inf")   # “no day booked yet”
    meetings = 0

    for start, end in slots:
        if next_free < start:   # jump to first legal day in the interval
            next_free = start
        if next_free <= end:    # slot fits → book it
            meetings += 1
            next_free += 1      # block that day

    return meetings

def _signature(word: str) -> str:
    return "".join(sorted(word))

# ─────────────────────────────────────────────────────────
# Task 2 – phrase counts by anagram substitution
# ─────────────────────────────────────────────────────────
def substitutions(words: List[str], phrases: List[str]) -> List[int]:
    # ── 1. Global array-size constraints ────────────────────────────
    words_amount = len(words)
    if not (0 < words_amount <= 100_000):
        raise ValueError(f"len(words) = {words_amount} must be 1 … 100 000")

    phrases_amount = len(phrases)
    if not (1 <= phrases_amount <= 1_000):
        raise ValueError(f"len(phrases) = {phrases_amount} must be 1 … 1 000")

    # ── 2. Per-word constraints (dictionary) ─────────────────────────
    dictionary_set = set(words)
    for i, w in enumerate(words):
        if not (1 <= len(w) <= 20):
            raise ValueError(
                f"words[{i}] length = {len(w)} (must be 1 … 20)"
            )

    # ── 3. Per-phrase constraints ──────────────────────────────────
    for phrase_index, phrase in enumerate(phrases):
        phrase_words = phrase.split()
        phrase_words_amount = len(phrase_words)
        if not (3 <= phrase_words_amount <= 20):
            raise ValueError(
                f"phrases[{phrase_index}] has {phrase_words_amount} words (must be 3 … 20)"
            )
        for word_index, word in enumerate(words):
            if word not in dictionary_set:
                raise ValueError(
                    f'Word "{word}" at phrases[{word_index}][{word_index}] '
                    "is not present in words[]"
                )

    # ── 4. Pre-processing: build signature → count table ────────────
    sig_count = Counter(_signature(w) for w in words)

    # ── 5. Evaluate every phrase ───────────────────
    results: List[int] = []
    for phrase in phrases:
        prod = 1
        for token in phrase.split():
            prod *= sig_count[_signature(token)]
            if prod == 0:
                break
        results.append(prod)

    return results


# ─────────────────────────────────────────────────────────
# Simple smoke-tests
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Task 1 example
    first_days = [1, 2, 3, 3, 3]
    last_days  = [2, 2, 3, 4, 4]
    print("Meetings that can be scheduled:",
          count_meetings(first_days, last_days))          # → 4

    # Task 2 example
    dictionary = ["desserts", "stressed", "bats", "stabs", "are", "not"]
    test_phrases = ["bats are not stressed"]
    print("Substitution counts:",
          substitutions(dictionary, test_phrases))        # → [2]
