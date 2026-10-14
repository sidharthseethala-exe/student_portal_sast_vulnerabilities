from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import json
import os

key = get_random_bytes(16)
iv = get_random_bytes(16)

plaintext = b"Padding oracle attack is interesting!"

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

with open("secret_key.bin", "wb") as f:
    f.write(key)

with open("public_data.json", "w") as f:
    json.dump({
        "iv": iv.hex(),
        "ciphertext": ciphertext.hex()
    }, f, indent=4)

os.chmod("secret_key.bin", 0o600)

print("AES-CBC encryption completed.")
print("IV:", iv.hex())
print("Ciphertext:", ciphertext.hex())
print("Ciphertext length:", len(ciphertext), "bytes")
print("Public data saved in public_data.json")
print("Secret key saved separately.")
