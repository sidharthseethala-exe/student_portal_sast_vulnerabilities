from http.server import HTTPServer, BaseHTTPRequestHandler
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

with open("secret_key.bin", "rb") as f:
    key = f.read() # knows it but attacker cannot acess it

class OracleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/oracle":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))

        try:
            iv = bytes.fromhex(data["iv"])
            ciphertext = bytes.fromhex(data["ciphertext"])

            if len(iv) != 16 or len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
                valid = False
            else:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = cipher.decrypt(ciphertext)

                try:
                    unpad(plaintext, AES.block_size)
                    valid = True
                except ValueError:
                    valid = False

        except (ValueError, KeyError, TypeError):
            valid = False

        response = json.dumps({"valid": valid}).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        return

server = HTTPServer(("127.0.0.1", 8000), OracleHandler)

print("Padding oracle is running on http://127.0.0.1:8000")
print("Press Ctrl+C to stop.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nOracle stopped.")
    server.server_close()
