from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from scipy.stats import chisquare, binomtest


# ------------------------------------------------------------
# Project folders and experiment settings
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
PLOTS_DIR = BASE_DIR / "plots"

MIN_BYTES = 1024 * 1024

SOURCES = {
    "Linux /dev/urandom": DATA_DIR / "urandom.bin",
    "OpenSSL rand": DATA_DIR / "openssl.bin",
    "Windows CNG": DATA_DIR / "windows_cng.bin",
}


# ------------------------------------------------------------
# Small helper functions
# ------------------------------------------------------------

def ensure_folders():
    """Create the output folders if they do not exist."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def longest_run(values):
    """Return the length of the longest run of equal values."""
    if len(values) == 0:
        return 0

    longest = 1
    current = 1

    for index in range(1, len(values)):
        if values[index] == values[index - 1]:
            current += 1
        else:
            longest = max(longest, current)
            current = 1

    return max(longest, current)


def lag_one_correlation(values):
    """
    Calculate Pearson correlation between adjacent byte values.
    The result is descriptive, not a cryptographic security test.
    """
    if len(values) < 2:
        return float("nan")

    left = values[:-1].astype(np.float64)
    right = values[1:].astype(np.float64)

    if np.std(left) == 0 or np.std(right) == 0:
        return float("nan")

    return float(np.corrcoef(left, right)[0, 1])


def repeated_pair_count(values):
    """
    Count repeated adjacent byte pairs.

    For example, if a two-byte sequence occurs 10 times,
    9 of those occurrences are repetitions beyond the first.
    """
    if len(values) < 2:
        return 0

    pairs = (
        values[:-1].astype(np.uint16) * 256
        + values[1:].astype(np.uint16)
    )

    counts = np.bincount(pairs, minlength=65536)

    return int(np.maximum(counts - 1, 0).sum())


# ------------------------------------------------------------
# Load and validate files
# ------------------------------------------------------------

def load_data():
    """Read the generated files and check their sizes."""
    loaded = {}

    for name, file_path in SOURCES.items():
        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing file: {file_path}\n"
                f"Generate the random data before running the analysis."
            )

        raw_bytes = file_path.read_bytes()

        if len(raw_bytes) < MIN_BYTES:
            raise ValueError(
                f"{file_path.name} contains only {len(raw_bytes)} bytes. "
                f"At least {MIN_BYTES} bytes are required."
            )

        values = np.frombuffer(raw_bytes, dtype=np.uint8)

        loaded[name] = values

        print(f"Loaded {name}: {len(values):,} bytes")

    return loaded


# ------------------------------------------------------------
# Statistical analysis
# ------------------------------------------------------------

def analyse_source(name, values):
    """Calculate descriptive statistics and selected test results."""
    byte_count = len(values)

    # Count the occurrence of each possible byte value.
    byte_counts = np.bincount(values, minlength=256)

    expected_byte_count = byte_count / 256

    byte_chi_square, byte_p_value = chisquare(
        byte_counts,
        f_exp=np.full(256, expected_byte_count)
    )

    # Inspect every bit in the byte stream.
    bits = np.unpackbits(values)

    ones = int(bits.sum())
    total_bits = int(bits.size)
    zeros = total_bits - ones

    bit_proportion = ones / total_bits

    # Under an ideal independent, unbiased-bit model,
    # the number of ones follows Binomial(total_bits, 0.5).
    bit_test = binomtest(
        ones,
        n=total_bits,
        p=0.5,
        alternative="two-sided"
    )

    # Runs test: count consecutive sequences of equal bits.
    observed_runs = 1 + int(np.count_nonzero(bits[1:] != bits[:-1]))

    n_ones = ones
    n_zeros = zeros

    # Exact expectation for the number of runs in a random
    # sequence with fixed counts of zeros and ones.
    expected_runs = (
        1 + (2 * n_ones * n_zeros / total_bits)
    )

    # Approximate standard deviation under the same model.
    run_variance = (
        2 * n_ones * n_zeros
        * (2 * n_ones * n_zeros - total_bits)
        / (total_bits ** 2 * (total_bits - 1))
    )

    if run_variance > 0:
        run_z_score = (
            observed_runs - expected_runs
        ) / np.sqrt(run_variance)
    else:
        run_z_score = float("nan")

    # Count repeated adjacent bytes and repeated adjacent pairs.
    repeated_bytes = int(np.count_nonzero(values[1:] == values[:-1]))

    repeated_pairs = repeated_pair_count(values)

    # Serial correlation for adjacent byte values.
    correlation = lag_one_correlation(values)

    # Approximate standard error for correlation under an
    # independent-data model.
    if byte_count > 2:
        correlation_z_score = correlation * np.sqrt(byte_count - 1)
    else:
        correlation_z_score = float("nan")

    # Longest run of identical bytes and bits.
    longest_byte_run = longest_run(values)
    longest_bit_run = longest_run(bits)

    return {
        "source": name,
        "bytes": byte_count,
        "bits": total_bits,
        "zero_bits": zeros,
        "one_bits": ones,
        "one_bit_percentage": bit_proportion * 100,
        "bit_binomial_p": float(bit_test.pvalue),
        "byte_chi_square": float(byte_chi_square),
        "byte_chi_square_p": float(byte_p_value),
        "observed_bit_runs": observed_runs,
        "expected_bit_runs": float(expected_runs),
        "bit_runs_z_score": float(run_z_score),
        "repeated_adjacent_bytes": repeated_bytes,
        "repeated_adjacent_pairs": repeated_pairs,
        "longest_identical_byte_run": longest_byte_run,
        "longest_identical_bit_run": longest_bit_run,
        "lag1_serial_correlation": correlation,
        "lag1_correlation_z_score": correlation_z_score,
    }, byte_counts, bits


# ------------------------------------------------------------
# Graph generation
# ------------------------------------------------------------

def create_byte_frequency_plot(byte_tables):
    """Plot the distribution of all 256 possible byte values."""
    fig, axes = plt.subplots(
        len(byte_tables),
        1,
        figsize=(13, 3.6 * len(byte_tables)),
        sharex=True
    )

    if len(byte_tables) == 1:
        axes = [axes]

    for axis, (name, counts) in zip(axes, byte_tables.items()):
        axis.bar(
            np.arange(256),
            counts,
            width=1.0,
            color="steelblue"
        )

        axis.axhline(
            counts.sum() / 256,
            color="red",
            linestyle="--",
            label="Expected frequency"
        )

        axis.set_title(name)
        axis.set_ylabel("Count")
        axis.legend()

    axes[-1].set_xlabel("Byte value (0–255)")

    fig.suptitle("Byte-frequency distributions")
    fig.tight_layout()

    fig.savefig(
        PLOTS_DIR / "byte_frequency.png",
        dpi=160
    )

    plt.close(fig)


def create_bit_distribution_plot(summaries):
    """Compare the percentage of zero and one bits."""
    names = [item["source"] for item in summaries]

    zero_percentages = [
        item["zero_bits"] / item["bits"] * 100
        for item in summaries
    ]

    one_percentages = [
        item["one_bits"] / item["bits"] * 100
        for item in summaries
    ]

    x = np.arange(len(names))
    width = 0.36

    fig, axis = plt.subplots(figsize=(10, 5))

    axis.bar(
        x - width / 2,
        zero_percentages,
        width,
        label="Zero bits",
        color="slateblue"
    )

    axis.bar(
        x + width / 2,
        one_percentages,
        width,
        label="One bits",
        color="darkorange"
    )

    axis.axhline(
        50,
        color="black",
        linestyle="--",
        linewidth=1
    )

    axis.set_xticks(x)
    axis.set_xticklabels(names, rotation=12, ha="right")
    axis.set_ylabel("Percentage (%)")
    axis.set_title("Bit distribution")
    axis.legend()

    fig.tight_layout()

    fig.savefig(
        PLOTS_DIR / "bit_distribution.png",
        dpi=160
    )

    plt.close(fig)


def create_correlation_plot(summaries):
    """Plot adjacent-byte serial correlation."""
    names = [item["source"] for item in summaries]

    correlations = [
        item["lag1_serial_correlation"]
        for item in summaries
    ]

    fig, axis = plt.subplots(figsize=(9, 5))

    axis.bar(
        names,
        correlations,
        color="seagreen"
    )

    axis.axhline(0, color="black", linewidth=1)

    axis.set_ylabel("Pearson correlation")
    axis.set_title("Lag-1 serial correlation")
    axis.tick_params(axis="x", rotation=12)

    fig.tight_layout()

    fig.savefig(
        PLOTS_DIR / "serial_correlation.png",
        dpi=160
    )

    plt.close(fig)


# ------------------------------------------------------------
# Save the detailed report
# ------------------------------------------------------------

def write_report(summaries):
    """Write a human-readable statistical report."""
    report_path = RESULTS_DIR / "statistical_report.txt"

    with report_path.open("w", encoding="utf-8") as report:
        report.write("OPERATING-SYSTEM RANDOMNESS EXPERIMENT\n")
        report.write("=" * 55 + "\n\n")

        report.write(
            "This report summarizes statistical measurements of "
            "random byte streams.\n"
        )

        report.write(
            "Statistical results are not proof of cryptographic security.\n\n"
        )

        for item in summaries:
            report.write("-" * 55 + "\n")
            report.write(f"Source: {item['source']}\n")
            report.write(f"Bytes analysed: {item['bytes']:,}\n")
            report.write(f"Bits analysed: {item['bits']:,}\n")

            report.write(
                f"Zero bits: {item['zero_bits']:,}\n"
            )

            report.write(
                f"One bits: {item['one_bits']:,}\n"
            )

            report.write(
                f"Percentage of one bits: "
                f"{item['one_bit_percentage']:.6f}%\n"
            )

            report.write(
                f"Bit binomial-test p-value: "
                f"{item['bit_binomial_p']:.6g}\n"
            )

            report.write(
                f"Byte chi-square statistic: "
                f"{item['byte_chi_square']:.6f}\n"
            )

            report.write(
                f"Byte chi-square p-value: "
                f"{item['byte_chi_square_p']:.6g}\n"
            )

            report.write(
                f"Observed bit runs: "
                f"{item['observed_bit_runs']:,}\n"
            )

            report.write(
                f"Expected bit runs: "
                f"{item['expected_bit_runs']:.3f}\n"
            )

            report.write(
                f"Bit-runs approximate z-score: "
                f"{item['bit_runs_z_score']:.6f}\n"
            )

            report.write(
                f"Repeated adjacent bytes: "
                f"{item['repeated_adjacent_bytes']:,}\n"
            )

            report.write(
                f"Repeated adjacent byte pairs: "
                f"{item['repeated_adjacent_pairs']:,}\n"
            )

            report.write(
                f"Longest identical-byte run: "
                f"{item['longest_identical_byte_run']}\n"
            )

            report.write(
                f"Longest identical-bit run: "
                f"{item['longest_identical_bit_run']}\n"
            )

            report.write(
                f"Lag-1 serial correlation: "
                f"{item['lag1_serial_correlation']:.8f}\n"
            )

            report.write(
                f"Lag-1 approximate z-score: "
                f"{item['lag1_correlation_z_score']:.6f}\n\n"
            )

        report.write(
            "INTERPRETATION\n"
            "---------------\n"
            "A p-value is not the probability that a generator is secure. "
            "It measures compatibility with a particular statistical "
            "null model. Small p-values can indicate a discrepancy, "
            "while large p-values do not prove randomness. "
            "Multiple tests, sample size, dependencies, and the "
            "cryptographic design must also be considered.\n"
        )

    print(f"Saved report: {report_path}")


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

def main():
    ensure_folders()

    print("\nLoading random-data files...\n")

    datasets = load_data()

    summaries = []
    byte_tables = {}
    bit_tables = {}

    for name, values in datasets.items():
        print(f"\nAnalysing: {name}")

        summary, byte_counts, bits = analyse_source(
            name,
            values
        )

        summaries.append(summary)
        byte_tables[name] = byte_counts

        bit_counts = np.bincount(bits, minlength=2)

        bit_tables[name] = bit_counts

        print(
            f"  Byte chi-square p-value: "
            f"{summary['byte_chi_square_p']:.6g}"
        )

        print(
            f"  Bit binomial-test p-value: "
            f"{summary['bit_binomial_p']:.6g}"
        )

        print(
            f"  One-bit percentage: "
            f"{summary['one_bit_percentage']:.6f}%"
        )

        print(
            f"  Lag-1 correlation: "
            f"{summary['lag1_serial_correlation']:.8f}"
        )

    # Save the summary table.
    summary_frame = pd.DataFrame(summaries)

    summary_frame.to_csv(
        RESULTS_DIR / "summary.csv",
        index=False
    )

    # Save the frequency of every byte value.
    frequency_rows = []

    for name, counts in byte_tables.items():
        for byte_value, count in enumerate(counts):
            frequency_rows.append({
                "source": name,
                "byte_value": byte_value,
                "count": int(count),
                "percentage": float(
                    count / counts.sum() * 100
                ),
            })

    pd.DataFrame(frequency_rows).to_csv(
        RESULTS_DIR / "byte_frequencies.csv",
        index=False
    )

    # Save zero/one bit counts.
    bit_rows = []

    for name, counts in bit_tables.items():
        total = int(counts.sum())

        for bit_value, count in enumerate(counts):
            bit_rows.append({
                "source": name,
                "bit_value": bit_value,
                "count": int(count),
                "percentage": float(count / total * 100),
            })

    pd.DataFrame(bit_rows).to_csv(
        RESULTS_DIR / "bit_frequencies.csv",
        index=False
    )

    # Create the graphs and written report.
    create_byte_frequency_plot(byte_tables)
    create_bit_distribution_plot(summaries)
    create_correlation_plot(summaries)
    write_report(summaries)

    print("\nExperiment completed.")
    print(f"Results folder: {RESULTS_DIR}")
    print(f"Plots folder: {PLOTS_DIR}")


if __name__ == "__main__":
    main()

