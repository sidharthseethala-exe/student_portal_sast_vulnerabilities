#include <iostream>
#include <string>
#include <cctype>

using namespace std;

string encrypt_text(const string &plaintext, const string &key) {
    string ciphertext = "";

    for (char ch : plaintext) {
        if (isalpha(ch)) {
            char upper = toupper(ch);
            char encrypted = key[upper - 'A'];

            if (islower(ch))
                ciphertext += tolower(encrypted);
            else
                ciphertext += encrypted;
        }
        else {
            ciphertext += ch;
        }
    }

    return ciphertext;
}

int main() {

    string plaintext;

    cout << "Enter plaintext: ";
    getline(cin, plaintext);

    string key = "QWERTYUIOPASDFGHJKLZXCVBNM";

    string ciphertext = encrypt_text(plaintext, key);

    cout << "\nPlaintext:\n";
    cout << plaintext << "\n";

    cout << "\nCiphertext:\n";
    cout << ciphertext << "\n";

    return 0;
}
