from pathlib import Path
from shift_cipher import decrypt

DICTIONARY_PATH = Path(__file__).parent.parent / "dictionary" / "english_words.txt"


def load_dictionary():
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return {word.strip().lower() for word in file if word.strip()}


def dictionary_score(text, dictionary):
    words = text.lower().split()
    return sum(1 for word in words if word in dictionary)


def dictionary_attack(ciphertext):
    dictionary = load_dictionary()

    best_key = 0
    best_plaintext = ""
    best_score = -1

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = dictionary_score(plaintext, dictionary)

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


if __name__ == "__main__":
    ciphertext = "WKLV LV D VHFUHW PHVVDJH"

    key, plaintext, score = dictionary_attack(ciphertext)

    print("Best Key:", key)
    print("Best Plaintext:", plaintext)
    print("Dictionary Score:", score)