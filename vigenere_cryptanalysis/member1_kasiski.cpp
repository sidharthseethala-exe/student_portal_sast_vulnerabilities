#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cctype>
#include <iomanip>
#include <algorithm>

using namespace std;

// =====================================================
// MEMBER 1 - VIGENERE CIPHER CRYPTANALYSIS
// KASISKI EXAMINATION + INDEX OF COINCIDENCE
// =====================================================


// =====================================================
// 1. CLEAN CIPHERTEXT
// Remove spaces/special characters and convert to uppercase
// =====================================================

string clean_ciphertext(string ciphertext)
{
    string clean = "";

    for (char c : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(c)))
        {
            clean += toupper(static_cast<unsigned char>(c));
        }
    }

    return clean;
}


// =====================================================
// 2. FIND REPEATED PATTERNS
// Find repeated sequences of length 3, 4 and 5
// Store pattern and positions where it occurs
// =====================================================

map<string, vector<int>> find_repeated_patterns(string ciphertext)
{
    map<string, vector<int>> patterns;

    // Search for patterns of length 3, 4 and 5
    for (int length = 3; length <= 5; length++)
    {
        for (int i = 0;
             i <= static_cast<int>(ciphertext.length()) - length;
             i++)
        {
            string pattern = ciphertext.substr(i, length);

            patterns[pattern].push_back(i);
        }
    }

    return patterns;
}


// =====================================================
// 3. CALCULATE DISTANCES
// Find distances between repeated occurrences
// =====================================================

vector<int> calculate_distances(
    map<string, vector<int>> &patterns)
{
    vector<int> distances;

    for (auto &p : patterns)
    {
        // Only consider patterns occurring more than once
        if (p.second.size() < 2)
        {
            continue;
        }

        vector<int> positions = p.second;

        // Calculate distance between every pair
        for (int i = 0; i < static_cast<int>(positions.size()); i++)
        {
            for (int j = i + 1;
                 j < static_cast<int>(positions.size());
                 j++)
            {
                int distance =
                    positions[j] - positions[i];

                distances.push_back(distance);
            }
        }
    }

    return distances;
}


// =====================================================
// 4. FIND FACTORS
// Find possible key lengths from a distance
// =====================================================

vector<int> find_factors(int n)
{
    vector<int> factors;

    // Key length 1 is ignored
    for (int i = 2; i <= n; i++)
    {
        if (n % i == 0)
        {
            factors.push_back(i);
        }
    }

    return factors;
}


// =====================================================
// 5. KASISKI ANALYSIS
// Count factor occurrences and rank candidate key lengths
// =====================================================

map<int, int> kasiski_analysis(
    vector<int> &distances)
{
    map<int, int> factor_count;

    for (int distance : distances)
    {
        vector<int> factors =
            find_factors(distance);

        for (int factor : factors)
        {
            // Practical key-length range
            if (factor >= 2 && factor <= 20)
            {
                factor_count[factor]++;
            }
        }
    }

    return factor_count;
}


// =====================================================
// 6. CALCULATE INDEX OF COINCIDENCE
//
// IC = sum [fi * (fi - 1)] / [N * (N - 1)]
//
// English text usually has IC around 0.066.
// Random text is usually around 0.038.
// =====================================================

double calculate_ic(string text)
{
    int frequency[26] = {0};

    for (char c : text)
    {
        if (c >= 'A' && c <= 'Z')
        {
            frequency[c - 'A']++;
        }
    }

    int N = static_cast<int>(text.length());

    if (N <= 1)
    {
        return 0.0;
    }

    double numerator = 0.0;

    for (int i = 0; i < 26; i++)
    {
        numerator +=
            frequency[i] * (frequency[i] - 1);
    }

    double denominator =
        N * (N - 1);

    return numerator / denominator;
}


// =====================================================
// 7. SPLIT INTO GROUPS
// Divide ciphertext according to candidate key length
//
// Example for key length 4:
//
// Group 1 -> positions 0,4,8,12...
// Group 2 -> positions 1,5,9,13...
// Group 3 -> positions 2,6,10,14...
// Group 4 -> positions 3,7,11,15...
// =====================================================

vector<string> split_into_groups(
    string ciphertext,
    int keyLength)
{
    vector<string> groups(keyLength);

    for (int i = 0;
         i < static_cast<int>(ciphertext.length());
         i++)
    {
        groups[i % keyLength] += ciphertext[i];
    }

    return groups;
}


// =====================================================
// HELPER FUNCTION
// Calculate average IC for a particular key length
// =====================================================

double average_ic_for_key_length(
    string ciphertext,
    int keyLength)
{
    vector<string> groups =
        split_into_groups(ciphertext, keyLength);

    double totalIC = 0.0;
    int validGroups = 0;

    for (string group : groups)
    {
        if (group.length() > 1)
        {
            totalIC += calculate_ic(group);
            validGroups++;
        }
    }

    if (validGroups == 0)
    {
        return 0.0;
    }

    return totalIC / validGroups;
}


// =====================================================
// MAIN
// =====================================================

int main()
{
    string ciphertext;

    cout << "=============================================\n";
    cout << " VIGENERE CIPHER CRYPTANALYSIS\n";
    cout << " KASISKI EXAMINATION + FREQUENCY ANALYSIS\n";
    cout << "=============================================\n\n";

    cout << "Enter ciphertext:\n";
    getline(cin, ciphertext);


    // =================================================
    // STEP 1: CLEAN CIPHERTEXT
    // =================================================

    string clean =
        clean_ciphertext(ciphertext);

    cout << "\n---------------------------------------------\n";
    cout << "1. CLEANED CIPHERTEXT\n";
    cout << "---------------------------------------------\n";

    cout << clean << endl;


    // =================================================
    // STEP 2: FIND REPEATED PATTERNS
    // =================================================

    map<string, vector<int>> patterns =
        find_repeated_patterns(clean);

    cout << "\n---------------------------------------------\n";
    cout << "2. REPEATED PATTERNS\n";
    cout << "---------------------------------------------\n";

    bool foundPattern = false;

    for (auto &p : patterns)
    {
        if (p.second.size() > 1)
        {
            foundPattern = true;

            cout << p.first << " : ";

            for (int position : p.second)
            {
                cout << position << " ";
            }

            cout << endl;
        }
    }

    if (!foundPattern)
    {
        cout << "No repeated patterns found.\n";
    }


    // =================================================
    // STEP 3: CALCULATE DISTANCES
    // =================================================

    vector<int> distances =
        calculate_distances(patterns);

    cout << "\n---------------------------------------------\n";
    cout << "3. DISTANCES BETWEEN REPEATED PATTERNS\n";
    cout << "---------------------------------------------\n";

    if (distances.empty())
    {
        cout << "No distances available.\n";
    }
    else
    {
        for (int distance : distances)
        {
            cout << distance << " ";
        }

        cout << endl;
    }


    // =================================================
    // STEP 4: FIND FACTORS
    // =================================================

    cout << "\n---------------------------------------------\n";
    cout << "4. FACTORS OF DISTANCES\n";
    cout << "---------------------------------------------\n";

    if (distances.empty())
    {
        cout << "No distances available.\n";
    }
    else
    {
        for (int distance : distances)
        {
            vector<int> factors =
                find_factors(distance);

            cout << "Distance "
                 << distance
                 << " : ";

            for (int factor : factors)
            {
                cout << factor << " ";
            }

            cout << endl;
        }
    }


    // =================================================
    // STEP 5: KASISKI ANALYSIS
    // =================================================

    map<int, int> factor_count =
        kasiski_analysis(distances);

    cout << "\n---------------------------------------------\n";
    cout << "5. KASISKI ANALYSIS\n";
    cout << "---------------------------------------------\n";

    if (factor_count.empty())
    {
        cout << "No candidate key lengths found.\n";
    }
    else
    {
        cout << left
             << setw(15)
             << "Key Length"
             << "Occurrences\n";

        cout << "-----------------------------\n";

        for (auto &p : factor_count)
        {
            cout << left
                 << setw(15)
                 << p.first
                 << p.second
                 << endl;
        }
    }


    // =================================================
    // STEP 6: INDEX OF COINCIDENCE ANALYSIS
    // =================================================

    cout << "\n---------------------------------------------\n";
    cout << "6. INDEX OF COINCIDENCE ANALYSIS\n";
    cout << "---------------------------------------------\n";

    cout << left
         << setw(15)
         << "Key Length"
         << "Average IC\n";

    cout << "-----------------------------\n";

    double bestIC = 0.0;
    int bestICLength = 0;

    for (int keyLength = 2;
         keyLength <= 20 &&
         keyLength <= static_cast<int>(clean.length());
         keyLength++)
    {
        double averageIC =
            average_ic_for_key_length(
                clean,
                keyLength);

        cout << left
             << setw(15)
             << keyLength
             << fixed
             << setprecision(4)
             << averageIC
             << endl;

        if (averageIC > bestIC)
        {
            bestIC = averageIC;
            bestICLength = keyLength;
        }
    }


    // =================================================
    // STEP 7: COMBINE KASISKI + IC
    //
    // Kasiski gives candidate lengths.
    // IC is used to confirm the strongest candidate.
    // =================================================

    cout << "\n---------------------------------------------\n";
    cout << "7. FINAL KEY LENGTH ESTIMATION\n";
    cout << "---------------------------------------------\n";

    cout << "Best IC candidate : "
         << bestICLength << endl;

    cout << "Best IC value     : "
         << fixed
         << setprecision(4)
         << bestIC << endl;


    // Find the strongest Kasiski candidates
    vector<pair<int, int>> kasiskiRanking;

    for (auto &p : factor_count)
    {
        kasiskiRanking.push_back(
            {p.first, p.second});
    }

    sort(
        kasiskiRanking.begin(),
        kasiskiRanking.end(),
        [](const pair<int, int> &a,
           const pair<int, int> &b)
        {
            if (a.second != b.second)
            {
                return a.second > b.second;
            }

            return a.first < b.first;
        });


    cout << "\nKasiski candidates ranked by occurrences:\n";

    int displayCount = 0;

    for (auto &p : kasiskiRanking)
    {
        cout << "Key Length "
             << p.first
             << " -> "
             << p.second
             << " occurrences"
             << endl;

        displayCount++;

        if (displayCount == 5)
        {
            break;
        }
    }


    // =================================================
    // FINAL DECISION
    //
    // If the strongest IC candidate also appears in
    // the Kasiski candidates, select it.
    // Otherwise use the strongest IC candidate.
    // =================================================

    int estimatedKeyLength = bestICLength;

    bool icFoundInKasiski = false;

    for (auto &p : factor_count)
    {
        if (p.first == bestICLength)
        {
            icFoundInKasiski = true;
            break;
        }
    }

    if (icFoundInKasiski)
    {
        estimatedKeyLength = bestICLength;
    }
    else if (!kasiskiRanking.empty())
    {
        // IC is still preferred because it validates
        // whether groups resemble English text.
        estimatedKeyLength = bestICLength;
    }


    cout << "\n=============================================\n";
    cout << " ESTIMATED KEY LENGTH: "
         << estimatedKeyLength
         << endl;
    cout << "=============================================\n";


    // =================================================
    // STEP 8: SPLIT CIPHERTEXT INTO GROUPS
    // =================================================

    cout << "\n---------------------------------------------\n";
    cout << "8. CIPHERTEXT GROUPS\n";
    cout << "---------------------------------------------\n";

    if (estimatedKeyLength > 0)
    {
        vector<string> groups =
            split_into_groups(
                clean,
                estimatedKeyLength);

        for (int i = 0;
             i < static_cast<int>(groups.size());
             i++)
        {
            cout << "Group "
                 << i + 1
                 << " : "
                 << groups[i]
                 << endl;
        }
    }
    else
    {
        cout << "Unable to create groups.\n";
    }


    // =================================================
    // FINAL IC INFORMATION
    // =================================================

    cout << "\n---------------------------------------------\n";
    cout << "SUMMARY\n";
    cout << "---------------------------------------------\n";

    cout << "Clean ciphertext length : "
         << clean.length()
         << endl;

    cout << "Estimated key length    : "
         << estimatedKeyLength
         << endl;

    cout << "Best average IC         : "
         << fixed
         << setprecision(4)
         << bestIC
         << endl;


    cout << "\n=============================================\n";
    cout << " MEMBER 1 ANALYSIS COMPLETE\n";
    cout << "=============================================\n";

    return 0;
}