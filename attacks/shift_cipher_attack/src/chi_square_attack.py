from collections import Counter
import string

ENGLISH_FREQ = {
    'a': 8.17,
    'b': 1.49,
    'c': 2.78,
    'd': 4.25,
    'e': 12.70,
    'f': 2.23,
    'g': 2.02,
    'h': 6.09,
    'i': 6.97,
    'j': 0.15,
    'k': 0.77,
    'l': 4.03,
    'm': 2.41,
    'n': 6.75,
    'o': 7.51,
    'p': 1.93,
    'q': 0.10,
    'r': 5.99,
    's': 6.33,
    't': 9.06,
    'u': 2.76,
    'v': 0.98,
    'w': 2.36,
    'x': 0.15,
    'y': 1.97,
    'z': 0.07
}


def chi_square_score(text):
    letters = [c.lower() for c in text if c.isalpha()]
    total = len(letters)

    if total == 0:
        return float('inf')

    counts = Counter(letters)
    score = 0

    for letter in string.ascii_lowercase:
        observed = counts.get(letter, 0)
        expected = ENGLISH_FREQ[letter] * total / 100
        score += ((observed - expected) ** 2) / expected

    return score


def chi_square_attack(ciphertext, decrypt_function):
    best_key = 0
    best_plaintext = ""
    best_score = float('inf')

    for key in range(26):
        plaintext = decrypt_function(ciphertext, key)
        score = chi_square_score(plaintext)

        if score < best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score
