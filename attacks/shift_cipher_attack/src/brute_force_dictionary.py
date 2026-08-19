from shift_cipher import decrypt


def load_words():
    with open("../dictionary/english_words.txt", "r") as f:
        return set(word.strip().lower() for word in f)


def score(text, words):
    total = 0

    for word in text.lower().split():
        word = word.strip(".,!?;:")
        if word in words:
            total += 1

    return total


def dictionary_attack(ciphertext):
    words = load_words()

    best_key = 0
    best_text = ""
    best_score = -1

    for key in range(26):
        plain = decrypt(ciphertext, key)
        s = score(plain, words)

        if s > best_score:
            best_score = s
            best_key = key
            best_text = plain

    return best_key, best_text, best_score
