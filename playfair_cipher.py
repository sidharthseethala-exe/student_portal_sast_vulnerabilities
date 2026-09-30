from collections import Counter


def generate_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")

    key = ""
    for ch in keyword:
        if ch.isalpha() and ch not in key:
            key += ch

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in key:
            key += ch

    matrix = []
    for i in range(0, 25, 5):
        matrix.append(key[i:i + 5])

    return matrix


def prepare_plaintext(plaintext):
    plaintext = plaintext.upper()
    plaintext = "".join(ch for ch in plaintext if ch.isalpha())
    plaintext = plaintext.replace("J", "I")

    result = ""
    i = 0

    while i < len(plaintext):
        first = plaintext[i]

        if i + 1 >= len(plaintext):
            result += first + "X"
            i += 1
        elif plaintext[i] == plaintext[i + 1]:
            result += first + "X"
            i += 1
        else:
            result += first + plaintext[i + 1]
            i += 2

    return result


def create_digraphs(prepared_text):
    return [prepared_text[i:i + 2] for i in range(0, len(prepared_text), 2)]


def find_position(matrix, ch):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col


def playfair_encrypt(plaintext, matrix):
    digraphs = create_digraphs(plaintext)
    ciphertext = ""

    for a, b in digraphs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5]
            ciphertext += matrix[r2][(c2 + 1) % 5]

        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1]
            ciphertext += matrix[(r2 + 1) % 5][c2]

        else:
            ciphertext += matrix[r1][c2]
            ciphertext += matrix[r2][c1]

    return ciphertext


def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    digraphs = create_digraphs(ciphertext)

    for a, b in digraphs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5]
            plaintext += matrix[r2][(c2 - 1) % 5]

        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1]
            plaintext += matrix[(r2 - 1) % 5][c2]

        else:
            plaintext += matrix[r1][c2]
            plaintext += matrix[r2][c1]

    return plaintext


def digraph_frequency(ciphertext):
    digraphs = create_digraphs(ciphertext)
    frequency = Counter(digraphs)

    return frequency


def verify(ciphertext, decrypted_text, matrix):
    re_encrypted = playfair_encrypt(decrypted_text, matrix)

    if re_encrypted == ciphertext:
        return "SUCCESS"
    else:
        return "FAILED"


def main():
    keyword = "MONARCHY"
    plaintext = "INSTRUMENTS"

    matrix = generate_key_matrix(keyword)

    print("Key Matrix")
    for row in matrix:
        print(" ".join(row))

    prepared_text = prepare_plaintext(plaintext)

    print("\nPrepared Plaintext:")
    print(prepared_text)

    digraphs = create_digraphs(prepared_text)

    print("\nPrepared Digraphs:")
    print(" ".join(digraphs))

    ciphertext = playfair_encrypt(prepared_text, matrix)

    print("\nCiphertext:")
    print(ciphertext)

    decrypted_text = playfair_decrypt(ciphertext, matrix)

    print("\nDecrypted Text:")
    print(decrypted_text)

    frequency = digraph_frequency(ciphertext)

    print("\nDigraph Frequency:")
    for digraph, count in frequency.items():
        print(digraph, ":", count)

    result = verify(ciphertext, decrypted_text, matrix)

    print("\nVerification:")
    print(result)


if __name__ == "__main__":
    main()
