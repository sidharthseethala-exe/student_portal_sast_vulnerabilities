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

string extract_words(const string &text, string words[], int &word_count) {
    string current_word = "";
    word_count = 0;

    for (char ch : text) {
        if (isalpha(ch)) {
            current_word += toupper(ch);
        }
        else {
            if (!current_word.empty()) {
                words[word_count] = current_word;
                word_count++;
                current_word = "";
            }
        }
    }

    if (!current_word.empty()) {
        words[word_count] = current_word;
        word_count++;
    }

    return "";
}

void word_frequency_analysis(const string &ciphertext) {
    string words[1000];
    int word_count = 0;

    extract_words(ciphertext, words, word_count);

    cout << "\nWord Frequency Analysis:\n";
    cout << "-----------------------\n";

    cout << "\nOne-letter words:\n";
    for (int i = 0; i < word_count; i++) {
        if (words[i].length() == 1) {
            cout << words[i] << " ";
        }
    }

    cout << "\n\nTwo-letter words:\n";
    for (int i = 0; i < word_count; i++) {
        if (words[i].length() == 2) {
            cout << words[i] << " ";
        }
    }

    cout << "\n\nThree-letter words:\n";
    for (int i = 0; i < word_count; i++) {
        if (words[i].length() == 3) {
            cout << words[i] << " ";
        }
    }

    cout << "\n\nRepeated words:\n";

    bool found_repeated = false;

    for (int i = 0; i < word_count; i++) {
        bool already_checked = false;

        for (int k = 0; k < i; k++) {
            if (words[k] == words[i]) {
                already_checked = true;
                break;
            }
        }

        if (already_checked)
            continue;

        int count = 0;

        for (int j = 0; j < word_count; j++) {
            if (words[i] == words[j]) {
                count++;
            }
        }

        if (count > 1) {
            cout << words[i] << " -> " << count << " times\n";
            found_repeated = true;
        }
    }

    if (!found_repeated) {
        cout << "No repeated words found.\n";
    }
}

string get_pattern(const string &word) {
    string pattern = "";
    int assigned[26];

    for (int i = 0; i < 26; i++) {
        assigned[i] = -1;
    }

    int next_number = 0;

    for (char ch : word) {
        char upper = toupper(ch);
        int index = upper - 'A';

        if (assigned[index] == -1) {
            assigned[index] = next_number;
            next_number++;
        }

        pattern += char('0' + assigned[index]);
    }

    return pattern;
}

void pattern_analysis(const string &ciphertext) {
    string words[1000];
    int word_count = 0;

    extract_words(ciphertext, words, word_count);

    cout << "\nPattern Analysis:\n";
    cout << "-----------------\n";

    for (int i = 0; i < word_count; i++) {
        cout << words[i] << " -> " << get_pattern(words[i]) << "\n";
    }
}

void frequency_analysis(const string &ciphertext) {
    int frequency[26] = {0};
    int total_letters = 0;

    for (char ch : ciphertext) {
        if (isalpha(ch)) {
            char upper = toupper(ch);
            frequency[upper - 'A']++;
            total_letters++;
        }
    }

    int letters[26];

    for (int i = 0; i < 26; i++) {
        letters[i] = i;
    }

    for (int i = 0; i < 25; i++) {
        for (int j = i + 1; j < 26; j++) {
            if (frequency[letters[j]] > frequency[letters[i]]) {
                int temp = letters[i];
                letters[i] = letters[j];
                letters[j] = temp;
            }
        }
    }

    cout << "\nFrequency Analysis:\n";
    cout << "-------------------\n";
    cout << "Letter\tCount\tPercentage\n";

    for (int i = 0; i < 26; i++) {
        int index = letters[i];

        double percentage = 0.0;

        if (total_letters > 0)
            percentage = (frequency[index] * 100.0) / total_letters;

        cout << char('A' + index)
             << "\t"
             << frequency[index]
             << "\t"
             << percentage
             << "%\n";
    }

    cout << "\nMost frequent ciphertext letters:\n";

    int highest = frequency[letters[0]];

    if (highest == 0) {
        cout << "No alphabetic characters found.\n";
    }
    else {
        for (int i = 0; i < 26; i++) {
            int index = letters[i];

            if (frequency[index] == highest) {
                cout << char('A' + index) << " ";
            }
            else {
                break;
            }
        }

        cout << "(Frequency = " << highest << ")\n";
    }
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

    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    return 0;
}