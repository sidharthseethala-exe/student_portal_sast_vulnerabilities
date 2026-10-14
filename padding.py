from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# ============================================================
# Utility functions
# ============================================================

BLOCK_SIZE = 16


def pkcs7_pad(data):
    """Apply PKCS#7 padding for AES."""
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_length]) * padding_length


def pkcs7_unpad(data):
    """Remove PKCS#7 padding, raising ValueError if invalid."""
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padded data length")

    padding_length = data[-1]

    if not 1 <= padding_length <= BLOCK_SIZE:
        raise ValueError("Invalid PKCS#7 padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid PKCS#7 padding")

    return data[:-padding_length]


# ============================================================
# Encryption setup
# The key is used only by the encryption system and oracle.
# The attack function never receives the key.
# ============================================================

def encrypt_message(key, plaintext):
    """Encrypt a plaintext using AES-CBC."""
    iv = get_random_bytes(BLOCK_SIZE)
    padded_plaintext = pkcs7_pad(plaintext)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_plaintext)

    return iv, ciphertext


def create_padding_oracle(secret_key):
    """
    Create an oracle that reveals only whether PKCS#7 padding
    is valid. The secret key remains inside this function.
    """

    def oracle(iv, ciphertext):
        try:
            if len(iv) != BLOCK_SIZE:
                return False

            if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
                return False

            cipher = AES.new(secret_key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)

            pkcs7_unpad(decrypted)
            return True

        except (ValueError, TypeError):
            return False

    return oracle


# ============================================================
# Padding Oracle Attack
# The attack receives only the oracle, IV, and ciphertext.
# ============================================================

def padding_oracle_attack(iv, ciphertext, oracle):
    """
    Recover plaintext without knowing the AES key.

    Args:
        iv: 16-byte initialization vector.
        ciphertext: AES-CBC ciphertext.
        oracle: Function returning True for valid PKCS#7 padding.

    Returns:
        recovered_plaintext, number_of_oracle_queries
    """

    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be exactly 16 bytes")

    if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext must contain complete AES blocks")

    query_count = 0

    # Split the ciphertext into 16-byte blocks.
    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered_plaintext = bytearray()

    # Recover each plaintext block separately.
    for block_index, target_block in enumerate(blocks):

        # The preceding block can be the IV or a ciphertext block.
        if block_index == 0:
            original_previous = iv
        else:
            original_previous = blocks[block_index - 1]

        # Holds D_K(target_block), recovered one byte at a time.
        intermediate = bytearray(BLOCK_SIZE)

        # Recover bytes from right to left.
        for padding_length in range(1, BLOCK_SIZE + 1):

            byte_index = BLOCK_SIZE - padding_length

            # Construct a modified preceding block.
            modified_previous = bytearray(
                get_bytes_copy(original_previous)
            )

            # Force all already-recovered suffix bytes to equal
            # the desired PKCS#7 padding value.
            for j in range(byte_index + 1, BLOCK_SIZE):
                modified_previous[j] = (
                    intermediate[j] ^ padding_length
                )

            found = False

            # Try every possible value of the intermediate byte.
            for candidate in range(256):

                modified_previous[byte_index] = (
                    candidate ^ padding_length
                )

                query_count += 1

                valid = oracle(
                    bytes(modified_previous),
                    target_block
                )

                if not valid:
                    continue

                # For padding length 1, eliminate accidental
                # matches caused by longer valid padding.
                if padding_length == 1:
                    confirmation = bytearray(modified_previous)

                    # Changing this byte should invalidate padding
                    # longer than 1, but not genuine 01 padding.
                    confirmation[-2] ^= 1

                    query_count += 1

                    if not oracle(
                        bytes(confirmation),
                        target_block
                    ):
                        continue

                intermediate[byte_index] = candidate
                found = True
                break

            if not found:
                raise RuntimeError(
                    f"Could not recover block {block_index}, "
                    f"byte {byte_index}"
                )

        # P_i = D_K(C_i) XOR C_(i-1)
        plaintext_block = bytes(
            intermediate[i] ^ original_previous[i]
            for i in range(BLOCK_SIZE)
        )

        recovered_plaintext.extend(plaintext_block)

    # Remove padding only after all blocks have been recovered.
    plaintext = pkcs7_unpad(bytes(recovered_plaintext))

    return plaintext, query_count


def get_bytes_copy(data):
    """Return a mutable bytearray copy of bytes."""
    return bytearray(data)


# ============================================================
# Demonstration
# ============================================================

def main():
    # This key belongs to the simulated encryption system.
    # It is never passed to padding_oracle_attack().
    secret_key = get_random_bytes(32)

    # Replace this sample message with your own test plaintext.
    original_plaintext = (
        b"Padding oracle attacks recover plaintext "
        b"without knowing the AES key."
    )

    # Encrypt the message.
    iv, ciphertext = encrypt_message(
        secret_key,
        original_plaintext
    )

    # Create the black-box padding oracle.
    oracle = create_padding_oracle(secret_key)

    print("AES-CBC Padding Oracle Attack")
    print("-" * 40)

    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Ciphertext length:", len(ciphertext), "bytes")

    # The attack receives no key.
    recovered_plaintext, query_count = padding_oracle_attack(
        iv,
        ciphertext,
        oracle
    )

    print("\nOriginal plaintext:", original_plaintext)
    print("Recovered plaintext:", recovered_plaintext)

    print("\nRecovered plaintext (UTF-8):")
    print(recovered_plaintext.decode("utf-8"))

    print("\nTotal oracle queries:", query_count)

    print(
        "\nAttack successful:",
        recovered_plaintext == original_plaintext
    )


if __name__ == "__main__":
    main()
