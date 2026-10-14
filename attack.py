import json
import urllib.request
import urllib.error

with open("public_data.json", "r") as f:
    data = json.load(f)

iv = bytes.fromhex(data["iv"])
ciphertext = bytes.fromhex(data["ciphertext"])

BLOCK_SIZE = 16
ORACLE_URL = "http://127.0.0.1:8000/oracle"
queries = 0

def padding_oracle(test_iv, test_ciphertext): #communication functon
    global queries

    request_data = json.dumps({ #cont the data we want to send server
        "iv": test_iv.hex(),
        "ciphertext": test_ciphertext.hex()
    }).encode()

    request = urllib.request.Request( # creates http req    
        ORACLE_URL,
        data=request_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode())
            queries += 1
            return result["valid"]
    except (urllib.error.URLError, TimeoutError) as e:
        raise RuntimeError(
            "Could not contact the oracle. Start oracle_server.py first."
        ) from e

def recover_block(previous_block, target_block, prefix):
    intermediate = bytearray(BLOCK_SIZE) # D(Ci)
    recovered = bytearray(BLOCK_SIZE) # XOR Ci-1

    for position in range(BLOCK_SIZE - 1, -1, -1):
        padding_value = BLOCK_SIZE - position
        modified = bytearray(previous_block)

        for j in range(position + 1, BLOCK_SIZE):
            modified[j] = intermediate[j] ^ padding_value #C'j = Ij XOR padding value

        found = False

        for guess in range(256):
            modified[position] = guess

            if prefix is None:
                test_iv = bytes(modified)
                test_ciphertext = target_block
            else:
                test_iv = iv
                test_blocks = bytearray(prefix)
                test_blocks[-BLOCK_SIZE:] = modified
                test_ciphertext = bytes(test_blocks) + target_block
                # lets the oracle process the target block using our modified previous block.
                #Original earlier blocks | Modified previous block | Target block

            if padding_oracle(test_iv, test_ciphertext): #flips one bit in the byte immediately before the current position.
                if position > 0:
                    check = bytearray(modified)
                    check[position - 1] ^= 1

                    if prefix is None:
                        check_iv = bytes(check)
                        check_ciphertext = target_block
                    else:
                        check_iv = iv
                        check_blocks = bytearray(prefix)
                        check_blocks[-BLOCK_SIZE:] = check
                        check_ciphertext = bytes(check_blocks) + target_block

                    if not padding_oracle(check_iv, check_ciphertext):
                        continue

                intermediate[position] = guess ^ padding_value
                recovered[position] = (
                    intermediate[position] ^ previous_block[position]
                )
                found = True
                break

        if not found:
            raise RuntimeError(
                "Could not recover byte at position " + str(position)
            )

    return bytes(recovered)

def recover_plaintext(iv, ciphertext):
    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    plaintext = bytearray()

    for block_index, target_block in enumerate(blocks):
        if block_index == 0:
            previous_block = iv
            prefix = None
        else:
            previous_block = blocks[block_index - 1]
            prefix = b"".join(blocks[:block_index])

        recovered = recover_block(
            previous_block,
            target_block,
            prefix
        )

        plaintext.extend(recovered)

        print(
            "Recovered block",
            block_index + 1,
            ":",
            recovered.hex()
        )

    padding_length = plaintext[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise RuntimeError("Recovered plaintext has invalid padding")

    if plaintext[-padding_length:] != bytes([padding_length]) * padding_length:
        raise RuntimeError("Recovered plaintext has invalid padding")

    return bytes(plaintext[:-padding_length])

print("Starting padding oracle attack...")
print("Ciphertext length:", len(ciphertext), "bytes")
print()

recovered_plaintext = recover_plaintext(iv, ciphertext)

print()
print("Recovered plaintext:", recovered_plaintext.decode("utf-8"))
print("Total oracle queries:", queries)

