def generate_key_matrix(keyword):

    keyword = keyword.upper()
    keyword = keyword.replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    key = "" # removing dub
    for char in keyword:
        if char.isalpha() and char not in key:
            key += char
            
    for char in alphabet:
        if char not in key:
            key += char

    matrix = []
    for i in range(0, 25, 5):
        matrix.append(list(key[i:i + 5]))
    return matrix



def prepare_plaintext(plaintext):
    plaintext = plaintext.upper()
    # only alphabetic characters
    plaintext = "".join(
        char for char in plaintext
        if char.isalpha()
    )
    plaintext = plaintext.replace("J", "I")
    return plaintext



def create_digraphs(plaintext):
    digraphs = []
    i = 0

    while i < len(plaintext):
        first = plaintext[i]

        # If there is another character
        if i + 1 < len(plaintext):
            second = plaintext[i + 1]

            # Repeated letters cannot be in the same pair
            if first == second:
                digraphs.append(first + "X")
                i += 1
            else:
                digraphs.append(first + second)
                i += 2

        else:
            # Odd-length plaintext gets X at the end
            digraphs.append(first + "X")
            i += 1

    return digraphs



def playfair_encrypt(digraphs, matrix):
    ciphertext = ""

    # creating a dictionary to quickly find letter positions
    positions = {}

    for row in range(5):
        for col in range(5):
            positions[matrix[row][col]] = (row, col)

    for pair in digraphs:
        first, second = pair

        row1, col1 = positions[first]
        row2, col2 = positions[second]

        # Rule 1: Same row
        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]

        # Rule 2: Same column
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]

        # Rule 3: Rectangle
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext


def playfair_decrypt(digraphs, matrix):
    pass
def digraph_frequency(ciphertext):
    pass
def verify(plaintext, matrix, ciphertext):
    pass
    
def main():
    keyword = "MONARCHY"
    plaintext = "INSTRUMENTS"

    matrix = generate_key_matrix(keyword)

    prepared = prepare_plaintext(plaintext)
    digraphs = create_digraphs(prepared)

    ciphertext = playfair_encrypt(digraphs, matrix)

    print("keyword:", keyword)
    print("plaintext:", plaintext)

    print("\nKey Matrix:")

    for row in matrix:
        print(" ".join(row))

    print("\nPrepared Digraphs:")
    print(" ".join(digraphs))

    print("\nCiphertext:")
    print(ciphertext)





if __name__ == "__main__":
    main()
