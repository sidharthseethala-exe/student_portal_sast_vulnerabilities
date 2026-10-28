import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import chisquare, binomtest, norm
import pandas as pd

files = {
    "Linux urandom": "urandom.bin",
    "OpenSSL": "openssl.bin",
    ".NET on Linux": "windows.bin"
}

results = []

for name, filename in files.items():
    with open(filename, "rb") as f:
        raw = f.read()

    arr = np.frombuffer(raw, dtype=np.uint8)

    print("\n==============================")
    print(name)
    print("File size:", len(raw), "bytes")

    # 1. Byte-frequency analysis
    observed = np.bincount(arr, minlength=256)
    expected = np.full(256, len(arr) / 256)

    chi_stat, chi_p = chisquare(observed, expected)

    print("\nBYTE FREQUENCY")
    print("Minimum frequency:", observed.min())
    print("Maximum frequency:", observed.max())
    print("Chi-square statistic:", chi_stat)
    print("Chi-square p-value:", chi_p)

    plt.figure()
    plt.bar(range(256), observed)
    plt.title(name + " - Byte Frequency")
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(name.replace(" ", "_") + "_frequency.png")
    plt.close()

    # 2. Bit-frequency analysis
    bits = np.unpackbits(arr)
    ones = int(bits.sum())
    zeros = len(bits) - ones

    bit_p = binomtest(
        ones, n=len(bits), p=0.5
    ).pvalue

    print("\nBIT FREQUENCY")
    print("Zeros:", zeros)
    print("Ones:", ones)
    print("Percentage of ones:", ones / len(bits) * 100)
    print("Binomial p-value:", bit_p)

    # 3. Repeated four-byte blocks
    blocks = [
        raw[i:i+4]
        for i in range(0, len(raw) - 3, 4)
    ]

    counts = Counter(blocks)
    repeated_values = sum(c > 1 for c in counts.values())

    print("\nREPEATED PATTERNS")
    print("Four-byte blocks:", len(blocks))
    print("Distinct blocks:", len(counts))
    print("Repeated block values:", repeated_values)

    # 4. Lag-1 serial correlation
    correlation = np.corrcoef(
        arr[:-1].astype(float),
        arr[1:].astype(float)
    )[0, 1]

    print("\nSERIAL CORRELATION")
    print("Lag-1 correlation:", correlation)

    # 5. Runs test
    n = len(bits)
    runs = 1 + np.count_nonzero(bits[1:] != bits[:-1])

    expected_runs = 1 + (2 * ones * zeros) / n

    variance = (
        2 * ones * zeros *
        (2 * ones * zeros - n)
    ) / (n**2 * (n - 1))

    z_score = (runs - expected_runs) / np.sqrt(variance)
    runs_p = 2 * norm.sf(abs(z_score))

    print("\nRUNS TEST")
    print("Observed runs:", runs)
    print("Expected runs:", expected_runs)
    print("Z-score:", z_score)
    print("Runs test p-value:", runs_p)

    results.append({
        "Source": name,
        "Bytes": len(raw),
        "Chi-square p-value": chi_p,
        "Bit-test p-value": bit_p,
        "Runs-test p-value": runs_p,
        "Lag-1 correlation": correlation,
        "Repeated 4-byte block values": repeated_values
    })

# 6. Comparison table
df = pd.DataFrame(results)

print("\n========== FINAL COMPARISON ==========")
print(df.to_string(index=False))

df.to_csv("random_analysis_results.csv", index=False)

print("\nResults saved to random_analysis_results.csv")
print("Frequency graphs saved as PNG files.")
