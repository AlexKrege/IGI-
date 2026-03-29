import string
from utils import simple_decorator

FIXED_TEXT = (
    "So she was considering in her own mind, as well as she could, for the "
    "hot day made her feel very sleepy and stupid, whether the pleasure of "
    "making a daisy-chain would be worth the trouble of getting up and "
    "picking the daisies, when suddenly a White Rabbit with pink eyes ran "
    "close by her."
)

def clean_and_split(text):
    """Remove punctuation (except apostrophe) and split into words."""
    for p in string.punctuation:
        if p != "'":
            text = text.replace(p, ' ')
    return [w for w in text.split() if w]

def words_with_odd_length(text):
    """Return list of words whose length is odd."""
    words = clean_and_split(text)
    return [w for w in words if len(w) % 2 == 1]

def shortest_word_starting_with_i(text):
    """Return the shortest word starting with 'i' (case‑insensitive)."""
    words = clean_and_split(text)
    candidates = [w for w in words if w.lower().startswith('i')]
    if not candidates:
        return None
    return min(candidates, key=len)

def find_duplicates(text):
    """Return list of words that appear more than once (case‑insensitive)."""
    words = [w.lower() for w in clean_and_split(text)]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, cnt in freq.items() if cnt > 1]

@simple_decorator
def run_task4():
    print("\n--- Task 4: Text Analysis ---")
    print("Analyzing the following text:")
    print(FIXED_TEXT)
    print()

    total = len(clean_and_split(FIXED_TEXT))
    odd_words = words_with_odd_length(FIXED_TEXT)
    print(f"a) Total words: {total}")
    print(f"   Words with odd length: {', '.join(odd_words)}")

    shortest = shortest_word_starting_with_i(FIXED_TEXT)
    if shortest:
        print(f"b) Shortest word starting with 'i': '{shortest}'")
    else:
        print("b) No word starts with 'i'.")

    duplicates = find_duplicates(FIXED_TEXT)
    if duplicates:
        print(f"c) Duplicate words (case‑insensitive): {', '.join(duplicates)}")
    else:
        print("c) No duplicate words found.")