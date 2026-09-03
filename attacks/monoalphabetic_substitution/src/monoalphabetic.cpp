#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>

using namespace std;

// ------------------------------------------------------------
// Convert character to uppercase
// ------------------------------------------------------------
char toUpperChar(char c) {
    if (c >= 'a' && c <= 'z')
        return c - 'a' + 'A';

    return c;
}

// ------------------------------------------------------------
// Read complete text from file
// ------------------------------------------------------------
string readFile(string filename) {

    ifstream file(filename);

    if (!file) {
        cout << "Error opening file: " << filename << endl;
        return "";
    }

    string text;
    string line;

    while (getline(file, line)) {
        text += line;
        text += '\n';
    }

    file.close();

    return text;
}

// ------------------------------------------------------------
// Apply substitution key
// key[i] = ciphertext for plaintext letter 'A' + i
// ------------------------------------------------------------
string encryptText(string plaintext, string key) {

    string ciphertext = "";

    for (char c : plaintext) {

        char upper = toUpperChar(c);

        if (upper >= 'A' && upper <= 'Z') {

            int index = upper - 'A';

            ciphertext += key[index];

        } else {

            ciphertext += c;
        }
    }

    return ciphertext;
}

// ------------------------------------------------------------
// Apply suspected substitutions to ciphertext
//
// cipherToPlain[ciphertext letter] = plaintext letter
// ------------------------------------------------------------
string apply_substitution(
    string ciphertext,
    char cipherLetter[],
    char plainLetter[]) {

    string result = "";

    for (char c : ciphertext) {

        char upper = toUpperChar(c);

        if (upper >= 'A' && upper <= 'Z') {

            int index = upper - 'A';

            if (cipherLetter[index] != '?')
                result += cipherLetter[index];
            else
                result += '_';

        } else {

            result += c;
        }
    }

    return result;
}

// ------------------------------------------------------------
// Frequency analysis
// ------------------------------------------------------------
void frequency_analysis(string ciphertext) {

    int freq[26] = {0};
    int total = 0;

    for (char c : ciphertext) {

        char upper = toUpperChar(c);

        if (upper >= 'A' && upper <= 'Z') {

            freq[upper - 'A']++;
            total++;
        }
    }

    vector<pair<char, int>> letters;

    for (int i = 0; i < 26; i++) {

        letters.push_back(
            make_pair('A' + i, freq[i])
        );
    }

    sort(
        letters.begin(),
        letters.end(),
        [](pair<char, int> a, pair<char, int> b) {
            return a.second > b.second;
        }
    );

    cout << "\n========== FREQUENCY ANALYSIS ==========\n";

    cout << "Letter\tCount\tPercentage\n";

    for (auto item : letters) {

        double percentage = 0;

        if (total > 0)
            percentage =
                (double)item.second / total * 100;

        cout << item.first << "\t"
             << item.second << "\t"
             << percentage << "%\n";
    }

    cout << "\nMost frequent letters:\n";

    for (int i = 0; i < 5; i++) {

        if (letters[i].second > 0) {

            cout << letters[i].first
                 << " (" << letters[i].second
                 << " occurrences)\n";
        }
    }
}

// ------------------------------------------------------------
// Word frequency analysis
// ------------------------------------------------------------
void word_frequency_analysis(string ciphertext) {

    map<string, int> wordCount;

    string word = "";

    for (int i = 0; i <= (int)ciphertext.length(); i++) {

        char c;

        if (i < (int)ciphertext.length())
            c = toUpperChar(ciphertext[i]);
        else
            c = ' ';

        if (c >= 'A' && c <= 'Z') {

            word += c;

        } else {

            if (!word.empty()) {

                wordCount[word]++;
                word = "";
            }
        }
    }

    cout << "\n========== WORD FREQUENCY ANALYSIS ==========\n";

    cout << "\nOne-letter words:\n";

    for (auto item : wordCount) {

        if (item.first.length() == 1)
            cout << item.first
                 << " -> "
                 << item.second << endl;
    }

    cout << "\nTwo-letter words:\n";

    for (auto item : wordCount) {

        if (item.first.length() == 2)
            cout << item.first
                 << " -> "
                 << item.second << endl;
    }

    cout << "\nThree-letter words:\n";

    for (auto item : wordCount) {

        if (item.first.length() == 3)
            cout << item.first
                 << " -> "
                 << item.second << endl;
    }

    cout << "\nRepeated words:\n";

    for (auto item : wordCount) {

        if (item.second > 1) {

            cout << item.first
                 << " -> "
                 << item.second << " times\n";
        }
    }
}

// ------------------------------------------------------------
// Generate word pattern
//
// Example:
// HELLO -> 01223
// THAT  -> 0123
// MEET  -> 0112
// ------------------------------------------------------------
string getPattern(string word) {

    map<char, int> patternMap;

    int nextNumber = 0;

    string pattern = "";

    for (char c : word) {

        if (patternMap.find(c) == patternMap.end()) {

            patternMap[c] = nextNumber;
            nextNumber++;
        }

        pattern +=
            char('0' + patternMap[c]);
    }

    return pattern;
}

// ------------------------------------------------------------
// Pattern analysis
// ------------------------------------------------------------
void pattern_analysis(string ciphertext) {

    map<string, int> patterns;

    string word = "";

    for (int i = 0; i <= (int)ciphertext.length(); i++) {

        char c;

        if (i < (int)ciphertext.length())
            c = toUpperChar(ciphertext[i]);
        else
            c = ' ';

        if (c >= 'A' && c <= 'Z') {

            word += c;

        } else {

            if (!word.empty()) {

                string pattern = getPattern(word);

                patterns[pattern]++;

                cout << word
                     << " -> "
                     << pattern << endl;

                word = "";
            }
        }
    }

    cout << "\nRepeated patterns:\n";

    for (auto item : patterns) {

        if (item.second > 1) {

            cout << item.first
                 << " -> "
                 << item.second
                 << " occurrences\n";
        }
    }
}

// ------------------------------------------------------------
// Display current partial plaintext
// ------------------------------------------------------------
void display_partial_plaintext(
    string ciphertext,
    char cipherLetter[],
    char plainLetter[]) {

    string result =
        apply_substitution(
            ciphertext,
            cipherLetter,
            plainLetter
        );

    cout << "\n========== PARTIAL PLAINTEXT ==========\n";
    cout << result << endl;
}

// ------------------------------------------------------------
// Add a suspected substitution
// ------------------------------------------------------------
bool addSubstitution(
    char cipherLetter[],
    char plainLetter[],
    char cipher,
    char plain) {

    cipher = toUpperChar(cipher);
    plain = toUpperChar(plain);

    if (cipher < 'A' || cipher > 'Z' ||
        plain < 'A' || plain > 'Z') {

        return false;
    }

    int cIndex = cipher - 'A';

    // Check if cipher letter already has mapping
    if (cipherLetter[cIndex] != '?') {

        if (cipherLetter[cIndex] == plain)
            return true;

        cout << "Cipher letter already mapped.\n";
        return false;
    }

    // Check that plaintext letter is not already used
    for (int i = 0; i < 26; i++) {

        if (cipherLetter[i] == plain) {

            cout << "Plaintext letter already used.\n";
            return false;
        }
    }

    cipherLetter[cIndex] = plain;
    plainLetter[plain - 'A'] = cipher;

    return true;
}

// ------------------------------------------------------------
// Interactive cryptanalysis
// ------------------------------------------------------------
void cryptanalysis(string ciphertext) {

    char cipherLetter[26];
    char plainLetter[26];

    for (int i = 0; i < 26; i++) {

        cipherLetter[i] = '?';
        plainLetter[i] = '?';
    }

    cout << "\n========== INTERACTIVE CRYPTANALYSIS ==========\n";

    cout << "\nEnter substitutions one at a time.\n";
    cout << "Example: Q E means Q -> E\n";
    cout << "Enter X X to stop.\n";

    while (true) {

        char cipher;
        char plain;

        cout << "\nCipher letter: ";
        cin >> cipher;

        cout << "Plain letter: ";
        cin >> plain;

        cipher = toUpperChar(cipher);
        plain = toUpperChar(plain);

        if (cipher == 'X' && plain == 'X')
            break;

        if (addSubstitution(
                cipherLetter,
                plainLetter,
                cipher,
                plain)) {

            cout << "Substitution accepted: "
                 << cipher
                 << " -> "
                 << plain
                 << endl;

            display_partial_plaintext(
                ciphertext,
                cipherLetter,
                plainLetter
            );

        } else {

            cout << "Substitution rejected.\n";
        }
    }

    cout << "\nFinal recovered plaintext:\n";

    display_partial_plaintext(
        ciphertext,
        cipherLetter,
        plainLetter
    );

    cout << "\nRecovered substitution key:\n";

    for (int i = 0; i < 26; i++) {

        cout << char('A' + i)
             << " -> ";

        if (cipherLetter[i] == '?')
            cout << "?";
        else
            cout << cipherLetter[i];

        cout << endl;
    }
}

// ------------------------------------------------------------
// Verify solution
// ------------------------------------------------------------
void verify_solution(
    string plaintext,
    string ciphertext,
    char cipherLetter[]) {

    char key[26];

    for (int i = 0; i < 26; i++)
        key[i] = '?';

    // cipherLetter[cipher] = plaintext
    // Convert to plaintext -> ciphertext key
    for (int i = 0; i < 26; i++) {

        if (cipherLetter[i] != '?') {

            char plain = cipherLetter[i];

            key[plain - 'A'] = 'A' + i;
        }
    }

    string recoveredCiphertext = "";

    for (char c : plaintext) {

        char upper = toUpperChar(c);

        if (upper >= 'A' && upper <= 'Z') {

            if (key[upper - 'A'] != '?')
                recoveredCiphertext +=
                    key[upper - 'A'];
            else
                recoveredCiphertext += '?';

        } else {

            recoveredCiphertext += c;
        }
    }

    cout << "\n========== VERIFICATION ==========\n";

    cout << "Original ciphertext:\n";
    cout << ciphertext << endl;

    cout << "\nRe-encrypted ciphertext:\n";
    cout << recoveredCiphertext << endl;

    if (recoveredCiphertext == ciphertext)
        cout << "\nVerification SUCCESSFUL.\n";
    else
        cout << "\nVerification FAILED or key is incomplete.\n";
}

// ------------------------------------------------------------
// Main
// ------------------------------------------------------------
int main() {

    string filename;

    cout << "Enter plaintext file name: ";
    cin >> filename;

    string plaintext = readFile(filename);

    if (plaintext.empty()) {

        cout << "No plaintext found.\n";
        return 0;
    }

    // Example substitution key.
    // Replace this with your own 26-letter permutation.
    string key =
        "QWERTYUIOPASDFGHJKLZXCVBNM";

    cout << "\n========== PLAINTEXT ==========\n";
    cout << plaintext << endl;

    string ciphertext =
        encryptText(plaintext, key);

    cout << "\n========== CIPHERTEXT ==========\n";
    cout << ciphertext << endl;

    frequency_analysis(ciphertext);

    word_frequency_analysis(ciphertext);

    cout << "\n========== PATTERN ANALYSIS ==========\n";

    pattern_analysis(ciphertext);

    cryptanalysis(ciphertext);

    return 0;
}
