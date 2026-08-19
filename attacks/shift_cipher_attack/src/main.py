from shift_cipher import decrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


def main():
    ciphertext = input("Enter ciphertext: ")

    dictionary_key, dictionary_plaintext, dictionary_score_value = dictionary_attack(ciphertext)

    chi_key, chi_plaintext, chi_score = chi_square_attack(ciphertext, decrypt)

    print("\nDictionary Scoring")
    print("Best Key:", dictionary_key)
    print("Best Plaintext:", dictionary_plaintext)
    print("Dictionary Score:", dictionary_score_value)

    print("\nChi-Square Analysis")
    print("Best Key:", chi_key)
    print("Best Plaintext:", chi_plaintext)
    print("Chi-Square Score:", chi_score)


if __name__ == "__main__":
    main()