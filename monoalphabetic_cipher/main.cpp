#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>

using namespace std;

// Read a file
string readFile(string fileName) {
    ifstream file(fileName);
    return string((istreambuf_iterator<char>(file)),
                   istreambuf_iterator<char>());
}

// Write to a file
void writeFile(string fileName, string text) {
    ofstream file(fileName);
    file << text;
}

// Encrypt plaintext
string encryptText(string text, string key) {
    string result = text;

    for (char &c : result) {
        if (isalpha(c)) {
            bool lower = islower(c);
            char x = toupper(c);

            x = key[x - 'A'];

            c = lower ? tolower(x) : x;
        }
    }

    return result;
}

// 1. Frequency Analysis
void frequency_analysis(string text) {
    map<char, int> freq;
    int total = 0;

    for (char c : text) {
        if (isalpha(c)) {
            freq[toupper(c)]++;
            total++;
        }
    }

    vector<pair<char, int>> v(freq.begin(), freq.end());

    sort(v.begin(), v.end(),
         [](auto &a, auto &b) {
             return a.second > b.second;
         });

    cout << "\nLETTER FREQUENCY\n";


    for (auto x : v) {
        double percent = (x.second * 100.0) / total;

        cout << x.first << " : "
             << x.second << " ("
             << percent << "%)\n";
    }

    if (!v.empty())
        cout << "\nMost frequent letter: "
             << v[0].first << endl;
}

// 2. Word Frequency Analysis
void word_frequency_analysis(string text) {
    map<string, int> freq;
    string word;

    for (char c : text) {
        if (isalpha(c))
            word += toupper(c);
        else if (!word.empty()) {
            freq[word]++;
            word.clear();
        }
    }

    if (!word.empty())
        freq[word]++;

    cout << "\nWORD ANALYSIS\n";

    cout << "\nOne-letter words:\n";
    for (auto x : freq)
        if (x.first.length() == 1)
            cout << x.first << " : " << x.second << endl;

    cout << "\nTwo-letter words:\n";
    for (auto x : freq)
        if (x.first.length() == 2)
            cout << x.first << " : " << x.second << endl;

    cout << "\nThree-letter words:\n";
    for (auto x : freq)
        if (x.first.length() == 3)
            cout << x.first << " : " << x.second << endl;

    cout << "\nRepeated words:\n";
    for (auto x : freq)
        if (x.second > 1)
            cout << x.first << " : " << x.second << endl;
}

// Generate pattern of a word
string getPattern(string word) {
    map<char, int> number;
    string pattern;
    int next = 0;

    for (char c : word) {
        if (!number.count(c))
            number[c] = next++;

        pattern += to_string(number[c]);
    }

    return pattern;
}

// 3. Pattern Analysis
void pattern_analysis(string text) {
    string word;

    cout << "\nPATTERN ANALYSIS\n";

    for (char c : text + " ") {
        if (isalpha(c)) {
            word += toupper(c);
        }
        else if (!word.empty()) {
            cout << word << " -> "
                 << getPattern(word) << endl;

            word.clear();
        }
    }
}

// Apply guessed substitutions
string apply_substitution(string cipher, map<char, char> key) {
    string result = cipher;

    for (char &c : result) {
        if (isalpha(c)) {
            char upper = toupper(c);

            if (key.count(upper))
                c = key[upper];
            else
                c = '_';
        }
    }

    return result;
}

// Display partial plaintext
void display_partial_plaintext(string cipher, map<char, char> key) {
    cout << "\nPARTIAL PLAINTEXT\n";
    cout << apply_substitution(cipher, key) << endl;
}

// 4. Verify solution
bool verify_solution(string plaintext,
                     string ciphertext,
                     string key) {

    string test = encryptText(plaintext, key);

    if (test == ciphertext) {
        cout << "\nVerification successful!\n";
        return true;
    }

    cout << "\nVerification failed!\n";
    return false;
}

int main() {

    string plaintext = readFile("plaintext.txt");

    // Plain alphabet -> cipher alphabet
    string key = "QWERTYUIOPASDFGHJKLZXCVBNM";

    // Encrypt
    string ciphertext = encryptText(plaintext, key);

    writeFile("ciphertext.txt", ciphertext);

    cout << "MONOALPHABETIC SUBSTITUTION CIPHER\n";

    int choice;

    do {
        cout << "\n1. Show Ciphertext";
        cout << "\n2. Frequency Analysis";
        cout << "\n3. Word Frequency Analysis";
        cout << "\n4. Pattern Analysis";
        cout << "\n5. Try Substitution";
        cout << "\n6. Verify Encryption";
        cout << "\n7. Exit";

        cout << "\n\nEnter choice: ";
        cin >> choice;

        if (choice == 1) {
            cout << "\nCIPHERTEXT\n";
            cout << ciphertext << endl;
        }

        else if (choice == 2) {
            frequency_analysis(ciphertext);
        }

        else if (choice == 3) {
            word_frequency_analysis(ciphertext);
        }

        else if (choice == 4) {
            pattern_analysis(ciphertext);
        }

        else if (choice == 5) {

            map<char, char> guessedKey;

            char cipherLetter, plainLetter;
            char again;

            do {
                cout << "\nEnter cipher letter: ";
                cin >> cipherLetter;

                cout << "Enter guessed plaintext letter: ";
                cin >> plainLetter;

                guessedKey[toupper(cipherLetter)]
                           = toupper(plainLetter);

                display_partial_plaintext(
                    ciphertext, guessedKey);

                cout << "\nAdd another substitution? (y/n): ";
                cin >> again;

            } while (again == 'y' || again == 'Y');
        }

        else if (choice == 6) {
            verify_solution(
                plaintext,
                ciphertext,
                key
            );
        }

    } while (choice != 7);

    cout << "\nProgram ended.\n";

    return 0;
}