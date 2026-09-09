from collections import Counter
import re


def clean_ciphertext(text):
    text = text.upper()
    return re.sub("[^A-Z]", "", text)


def find_repeated_patterns(text):
    patterns = {}

    for length in range(3, 6):
        for i in range(len(text) - length + 1):
            pattern = text[i:i + length]

            if pattern not in patterns:
                positions = []

                for j in range(len(text) - length + 1):
                    if text[j:j + length] == pattern:
                        positions.append(j)

                if len(positions) > 1:
                    patterns[pattern] = positions

    return patterns


def calculate_distances(patterns):
    distances = []

    for pattern in patterns:
        positions = patterns[pattern]

        for i in range(len(positions) - 1):
            distance = positions[i + 1] - positions[i]
            distances.append(distance)

    return distances


def find_factors(number):
    factors = []

    for i in range(2, number + 1):
        if number % i == 0:
            factors.append(i)

    return factors


def kasiski_analysis(distances):
    count = Counter()

    for distance in distances:
        factors = find_factors(distance)

        for factor in factors:
            if factor <= 20:
                count[factor] += 1

    return count.most_common()


def calculate_ic(text):
    n = len(text)

    if n <= 1:
        return 0

    count = Counter(text)
    total = 0

    for letter in count:
        total += count[letter] * (count[letter] - 1)

    return total / (n * (n - 1))


def split_into_groups(text, key_length):
    groups = []

    for i in range(key_length):
        group = text[i::key_length]
        groups.append(group)

    return groups


def frequency_analysis(group):
    count = Counter(group)

    print("\nA B C D E F G H I J K L M N O P Q R S T U V W X Y Z")

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(count[letter], end=" ")

    print()


def find_shift(group):
    english = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

    count = Counter(group)
    most_common = count.most_common()

    cipher_letter = most_common[0][0]
    plain_letter = "E"

    shift = (ord(cipher_letter) - ord(plain_letter)) % 26

    return shift


def find_key(groups):
    key = ""

    for group in groups:
        shift = find_shift(group)
        key += chr(65 + shift)

    return key


def vigenere_decrypt(ciphertext, key):
    plaintext = ""

    for i in range(len(ciphertext)):
        c = ord(ciphertext[i]) - 65
        k = ord(key[i % len(key)]) - 65

        p = (c - k) % 26

        plaintext += chr(p + 65)

    return plaintext


def vigenere_encrypt(plaintext, key):
    ciphertext = ""

    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - 65
        k = ord(key[i % len(key)]) - 65

        c = (p + k) % 26

        ciphertext += chr(c + 65)

    return ciphertext


def verify(original, encrypted):
    return original == encrypted


def main():

    ciphertext = """
    DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA
    MKTTF TCCFX
    KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP
    WFKLS LEASE
    PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW
    NUOVJ MJCLL
    OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ
    ZVRMN WTQSE
    OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM
    OECBX SESCI
    YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL
    RYELH QSVWB
    AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV
    OVVXH KWQIL
    IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE
    TZEDF
    """

    ciphertext = clean_ciphertext(ciphertext)

    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("-----------------------------")

    print("Ciphertext length:", len(ciphertext))

    patterns = find_repeated_patterns(ciphertext)

    print("\nREPEATED PATTERNS")

    for pattern in patterns:
        print(pattern, patterns[pattern])

    distances = calculate_distances(patterns)

    print("\nDISTANCES")
    print(distances)

    factors = kasiski_analysis(distances)

    print("\nKASISKI ANALYSIS")

    for factor, count in factors:
        print(factor, "appeared", count, "times")

    key_length = factors[0][0]

    print("\nEstimated key length:", key_length)

    print("\nINDEX OF COINCIDENCE")

    for length in range(1, 21):
        groups = split_into_groups(ciphertext, length)

        total = 0

        for group in groups:
            total += calculate_ic(group)

        average = total / len(groups)

        print(length, ":", round(average, 4))

    groups = split_into_groups(ciphertext, key_length)

    print("\nFREQUENCY ANALYSIS")

    for i in range(len(groups)):
        print("\nGroup", i + 1)
        print(groups[i])
        frequency_analysis(groups[i])

    key = find_key(groups)

    print("\nRecovered key:", key)

    plaintext = vigenere_decrypt(ciphertext, key)

    print("\nRECOVERED PLAINTEXT")
    print(plaintext)

    encrypted = vigenere_encrypt(plaintext, key)

    print("\nVERIFICATION")

    if verify(ciphertext, encrypted):
        print("Re-encryption successful.")
        print("Original and encrypted ciphertext are same.")
    else:
        print("Verification failed.")


main()
