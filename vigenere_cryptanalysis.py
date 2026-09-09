from collections import Counter
import re


# ============================================================
# VIGENERE CIPHER CRYPTANALYSIS
# KASISKI EXAMINATION + FREQUENCY ANALYSIS
# ============================================================


# English letter frequencies
ENGLISH_FREQ = [
    0.082, 0.015, 0.028, 0.043, 0.127,
    0.022, 0.020, 0.061, 0.070, 0.002,
    0.008, 0.040, 0.024, 0.067, 0.075,
    0.019, 0.001, 0.060, 0.063, 0.091,
    0.028, 0.010, 0.024, 0.002, 0.020,
    0.001
]


# ============================================================
# MEMBER 1 - KASISKI EXAMINATION
# ============================================================


# ------------------------------------------------------------
# 1. clean_ciphertext()
# Remove spaces/special characters and convert to uppercase
# ------------------------------------------------------------

def clean_ciphertext(text):

    text = text.upper()

    return re.sub(r"[^A-Z]", "", text)


# ------------------------------------------------------------
# 2. find_repeated_patterns()
# Find repeated sequences of length 3, 4 and 5
# ------------------------------------------------------------

def find_repeated_patterns(text):

    patterns = {}

    for length in range(3, 6):

        for i in range(len(text) - length + 1):

            pattern = text[i:i + length]

            positions = []

            for j in range(len(text) - length + 1):

                if text[j:j + length] == pattern:
                    positions.append(j)

            if len(positions) > 1:

                patterns[pattern] = positions

    return patterns


# ------------------------------------------------------------
# 3. calculate_distances()
# Calculate distances between repeated occurrences
# ------------------------------------------------------------

def calculate_distances(patterns):

    distances = []

    for pattern in patterns:

        positions = patterns[pattern]

        for i in range(len(positions) - 1):

            distance = positions[i + 1] - positions[i]

            distances.append(distance)

    return distances


# ------------------------------------------------------------
# 4. find_factors()
# Find factors of a distance
# ------------------------------------------------------------

def find_factors(number):

    factors = []

    for i in range(2, number + 1):

        if number % i == 0:

            factors.append(i)

    return factors


# ------------------------------------------------------------
# 5. kasiski_analysis()
# Count possible key lengths from distance factors
# ------------------------------------------------------------

def kasiski_analysis(distances):

    count = Counter()

    for distance in distances:

        factors = find_factors(distance)

        for factor in factors:

            # Key length candidates limited to 20
            if factor <= 20:

                count[factor] += 1

    return count


# ============================================================
# MEMBER 1 - INDEX OF COINCIDENCE
# ============================================================


# ------------------------------------------------------------
# 6. calculate_ic()
# Calculate Index of Coincidence
# ------------------------------------------------------------

def calculate_ic(text):

    n = len(text)

    if n <= 1:

        return 0.0

    frequencies = Counter(text)

    total = 0

    for frequency in frequencies.values():

        total += frequency * (frequency - 1)

    return total / (n * (n - 1))


# ------------------------------------------------------------
# 7. split_into_groups()
# Divide ciphertext according to key length
# ------------------------------------------------------------

def split_into_groups(text, key_length):

    groups = []

    for i in range(key_length):

        groups.append(text[i::key_length])

    return groups


# ============================================================
# MEMBER 2 - FREQUENCY ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 8. frequency_analysis()
# Calculate A-Z frequency for each group
# ------------------------------------------------------------

def frequency_analysis(group):

    count = Counter(group)

    print(
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    )

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        print(count[letter], end=" ")

    print()


# ------------------------------------------------------------
# 9. find_shift()
# Estimate Caesar shift using Chi-Square analysis
# ------------------------------------------------------------

def find_shift(group):

    n = len(group)

    if n == 0:

        return 0

    observed = Counter(group)

    best_shift = 0

    best_score = float("inf")

    # Try every possible Caesar shift
    for shift in range(26):

        chi_square = 0.0

        for cipher_index in range(26):

            cipher_letter = chr(65 + cipher_index)

            # Convert ciphertext letter back to plaintext
            plain_index = (cipher_index - shift) % 26

            observed_count = observed[cipher_letter]

            expected_count = ENGLISH_FREQ[plain_index] * n

            if expected_count > 0:

                chi_square += (
                    (observed_count - expected_count) ** 2
                    / expected_count
                )

        if chi_square < best_score:

            best_score = chi_square

            best_shift = shift

    return best_shift


# ------------------------------------------------------------
# 10. find_key()
# Combine shifts from all groups
# ------------------------------------------------------------

def find_key(groups):

    key = ""

    for group in groups:

        shift = find_shift(group)

        key += chr(65 + shift)

    return key


# ============================================================
# VIGENERE OPERATIONS
# ============================================================


# ------------------------------------------------------------
# 11. vigenere_decrypt()
# Decrypt ciphertext using recovered key
# ------------------------------------------------------------

def vigenere_decrypt(ciphertext, key):

    plaintext = ""

    for i in range(len(ciphertext)):

        c = ord(ciphertext[i]) - 65

        k = ord(key[i % len(key)]) - 65

        p = (c - k) % 26

        plaintext += chr(p + 65)

    return plaintext


# ------------------------------------------------------------
# 12. vigenere_encrypt()
# Re-encrypt plaintext using recovered key
# ------------------------------------------------------------

def vigenere_encrypt(plaintext, key):

    ciphertext = ""

    for i in range(len(plaintext)):

        p = ord(plaintext[i]) - 65

        k = ord(key[i % len(key)]) - 65

        c = (p + k) % 26

        ciphertext += chr(c + 65)

    return ciphertext


# ------------------------------------------------------------
# 13. verify()
# Check whether re-encryption matches original ciphertext
# ------------------------------------------------------------

def verify(original, encrypted):

    return original == encrypted


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    ciphertext = """
    DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA
    MKTTF TCCFX KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV
    GQSOH QSVHP WFKLS LEASE PWHMJ EGKPU RVSXJ XVBWV
    POSDE TEQTX OBZIK WCXLW NUOVJ MJCLL OEOFA ZENVM
    JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ ZVRMN WTQSE
    OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM
    OECBX SESCI YGUFP KVILL TWDKS ZODFW FWEAA PQTFS
    TQIRG MPMEL RYELH QSVWB AWMOS DELHM UZGPG YEKZU
    KWTAM ZJMLS EVJQT GLAWV OVVXH KWQIL IEUYS ZWXAH
    HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE TZEDF
    """

    # ========================================================
    # STEP 1 - PREPROCESS
    # ========================================================

    ciphertext = clean_ciphertext(ciphertext)

    print("=" * 55)
    print("       VIGENERE CIPHER CRYPTANALYSIS")
    print("   KASISKI EXAMINATION + FREQUENCY ANALYSIS")
    print("=" * 55)

    print("\n1. CLEANED CIPHERTEXT")
    print("-" * 55)

    print(ciphertext)

    print("\nCiphertext length:", len(ciphertext))


    # ========================================================
    # STEP 2 - REPEATED PATTERNS
    # ========================================================

    patterns = find_repeated_patterns(ciphertext)

    print("\n2. REPEATED PATTERNS")
    print("-" * 55)

    for pattern, positions in patterns.items():

        print(pattern, ":", positions)


    # ========================================================
    # STEP 3 - DISTANCES
    # ========================================================

    distances = calculate_distances(patterns)

    print("\n3. DISTANCES BETWEEN REPEATED PATTERNS")
    print("-" * 55)

    print(distances)


    # ========================================================
    # STEP 4 - FACTORS
    # ========================================================

    print("\n4. FACTORS OF DISTANCES")
    print("-" * 55)

    for distance in distances:

        print(
            "Distance",
            distance,
            ":",
            find_factors(distance)
        )


    # ========================================================
    # STEP 5 - KASISKI ANALYSIS
    # ========================================================

    kasiski_counts = kasiski_analysis(distances)

    print("\n5. KASISKI ANALYSIS")
    print("-" * 55)

    print("Key Length     Occurrences")
    print("--------------------------")

    for length, count in kasiski_counts.most_common():

        print(
            f"{length:<15}{count}"
        )


    # ========================================================
    # STEP 6 - INDEX OF COINCIDENCE
    # ========================================================

    print("\n6. INDEX OF COINCIDENCE")
    print("-" * 55)

    best_ic = -1

    best_ic_length = 0

    for length in range(2, 21):

        groups = split_into_groups(
            ciphertext,
            length
        )

        total_ic = 0

        for group in groups:

            total_ic += calculate_ic(group)

        average_ic = total_ic / len(groups)

        print(
            f"{length:<3} : {average_ic:.4f}"
        )

        if average_ic > best_ic:

            best_ic = average_ic

            best_ic_length = length


    # ========================================================
    # FINAL KEY LENGTH
    # ========================================================

    key_length = best_ic_length

    print("\n7. FINAL KEY LENGTH ESTIMATION")
    print("-" * 55)

    print(
        "Best IC candidate :",
        best_ic_length
    )

    print(
        "Best IC value     :",
        f"{best_ic:.4f}"
    )

    print(
        "Estimated key length:",
        key_length
    )


    # ========================================================
    # STEP 8 - SPLIT INTO GROUPS
    # ========================================================

    groups = split_into_groups(
        ciphertext,
        key_length
    )

    print("\n8. CIPHERTEXT GROUPS")
    print("-" * 55)

    for i, group in enumerate(groups):

        print(
            f"Group {i + 1} : {group}"
        )


    # ========================================================
    # STEP 9 - FREQUENCY ANALYSIS
    # ========================================================

    print("\n9. FREQUENCY ANALYSIS")
    print("-" * 55)

    for i, group in enumerate(groups):

        print(
            f"\nGroup {i + 1}"
        )

        frequency_analysis(group)


    # ========================================================
    # STEP 10 - SHIFT ANALYSIS
    # ========================================================

    print("\n10. SHIFT ANALYSIS")
    print("-" * 55)

    for i, group in enumerate(groups):

        shift = find_shift(group)

        key_letter = chr(65 + shift)

        print(
            f"Group {i + 1} "
            f"Shift = {shift} "
            f"Key letter = {key_letter}"
        )


    # ========================================================
    # STEP 11 - FIND KEY
    # ========================================================

    key = find_key(groups)

    print("\n11. RECOVERED KEY")
    print("-" * 55)

    print(key)


    # ========================================================
    # STEP 12 - DECRYPT
    # ========================================================

    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\n12. RECOVERED PLAINTEXT")
    print("-" * 55)

    print(plaintext)


    # ========================================================
    # STEP 13 - RE-ENCRYPT
    # ========================================================

    encrypted = vigenere_encrypt(
        plaintext,
        key
    )


    # ========================================================
    # STEP 14 - VERIFICATION
    # ========================================================

    print("\n13. VERIFICATION")
    print("-" * 55)

    if verify(ciphertext, encrypted):

        print("Re-encryption successful.")

        print(
            "Original and encrypted ciphertext are same."
        )

    else:

        print("Verification failed.")


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 55)
    print("                    SUMMARY")
    print("=" * 55)

    print(
        "Clean ciphertext length :",
        len(ciphertext)
    )

    print(
        "Estimated key length    :",
        key_length
    )

    print(
        "Recovered key           :",
        key
    )

    print(
        "Verification             :",
        "SUCCESS" if verify(ciphertext, encrypted)
        else "FAILED"
    )

    print("=" * 55)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
