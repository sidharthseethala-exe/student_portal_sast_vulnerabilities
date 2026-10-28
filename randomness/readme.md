
Experiment: Evaluation of Operating-System Random-Number Generation Mechanisms
1. Aim

To generate random data using Linux /dev/urandom, OpenSSL's rand utility, and Windows CNG through .NET, analyse their statistical properties, and evaluate their suitability for cryptographic applications.

2. Objectives
Generate at least 1 MiB of random data from each mechanism.
Analyse byte frequencies and bit distributions.
Examine repeated patterns and consecutive bit runs.
Calculate serial correlation.
Apply statistical tests and compare the results.
Understand why statistical randomness does not guarantee cryptographic security.
3. Requirements
Linux operating system.
Python 3.
OpenSSL.
Python libraries: NumPy, SciPy, Pandas, and Matplotlib.
Windows-generated binary data obtained using .NET CNG.
Jupyter Notebook for documenting and analysing results.
4. Theory

Random-number generators are important in cryptography for generating encryption keys, nonces, salts, and other security-sensitive values.

A cryptographically secure pseudorandom number generator (CSPRNG) produces output designed to be computationally unpredictable, even when an attacker knows previous outputs.

Mechanisms studied

Linux /dev/urandom: Provides random bytes through the Linux kernel's random-number subsystem, which gathers and processes entropy from available sources.

OpenSSL rand: Generates cryptographic random bytes using OpenSSL's random-number generation facilities, which use a cryptographic pseudorandom generator seeded and managed by the library.

Windows CNG through .NET: Uses Windows cryptographic services through .NET's cryptographic random-number API to obtain cryptographically secure random bytes.

Statistical methods
Byte-frequency analysis: Examines the frequencies of all 256 possible byte values.
Chi-square test: Tests whether observed byte frequencies differ significantly from a uniform distribution.
Bit-distribution analysis: Measures the proportions of zero and one bits.
Binomial test: Tests whether the observed number of one bits is consistent with a 50% probability.
Runs analysis: Examines consecutive groups of identical bits.
Repeated-pattern analysis: Identifies consecutive identical bytes and unusually long repeated sequences.
Serial correlation: Measures the linear relationship between adjacent byte values.
5. Experimental Procedure
Generated 1,048,576 bytes using Linux /dev/urandom.
Generated 1,048,576 bytes using OpenSSL's rand utility.
Obtained 1,048,576 bytes generated through Windows CNG using .NET.
Stored the datasets as binary files.
Loaded the files into a Python analysis program.
Calculated byte frequencies, bit proportions, statistical test results, repeated-pattern measurements, and serial correlations.
Generated CSV reports and graphical visualisations.
Compared the measurements to evaluate the statistical properties of the three datasets.
6. Experimental Results

Each dataset contained 1,048,576 bytes, equivalent to 8,388,608 bits.

Measurement	Linux /dev/urandom	OpenSSL rand	Windows CNG
Data size (bytes)	1,048,576	1,048,576	1,048,576
One-bit percentage	49.999857%	50.001347%	49.987221%
Bit binomial-test p-value	0.993664	0.938079	0.459356
Byte chi-square statistic	254.327637	236.633789	255.983887
Byte chi-square p-value	0.500106	0.789287	0.470892
Observed bit runs	4,193,589	4,191,286	4,192,501
Bit-runs Z-score	-0.494422	-2.084720	-1.245534
Repeated adjacent bytes	4,068	4,114	4,099
Longest identical byte run	3	3	3
Longest identical bit run	24	23	21
Lag-1 correlation	-0.000369	0.000399	0.000755

Note: The reported repeated-adjacent-pairs count was 983,039 for all three datasets. This measurement requires verification against the analysis code before being interpreted as a valid repeated-pattern count.

7. Analysis and Interpretation
A. Byte-frequency analysis

The chi-square p-values were 0.500106 for Linux, 0.789287 for OpenSSL, and 0.470892 for Windows CNG.

All values exceed the significance level of 0.05. Therefore, the tests did not provide sufficient evidence to reject the hypothesis that the byte values follow a uniform distribution.

B. Bit-distribution analysis

The one-bit percentages were approximately 50% for all three datasets. Their binomial-test p-values also exceeded 0.05.

This indicates that the observed proportions of zero and one bits are consistent with the specified unbiased-bit model.

C. Runs analysis

The observed number of bit runs was compared with the expected number for independent, unbiased bits.

The OpenSSL Z-score was -2.084720, indicating fewer runs than expected. This result warrants further investigation, including verification of the test implementation and its variance calculation.

D. Repeated-pattern analysis

The number of adjacent equal bytes ranged from 4,068 to 4,114, close to the expected count of approximately 4,096 for uniformly distributed independent bytes.

The longest identical byte run was three bytes for all datasets.

The repeated-adjacent-pairs metric requires verification because its reported value was identical across all three samples.

E. Serial correlation

The lag-1 correlation coefficients were close to zero for all three generators.

This indicates little observed linear correlation between adjacent byte values. However, the result does not rule out other forms of dependency or predictability.

8. Comparison of Linux and Windows Mechanisms

Linux /dev/urandom obtains random bytes from the kernel's random-number subsystem. OpenSSL uses its own cryptographic random-number generation facilities and obtains seed material from suitable system sources.

Windows CNG provides cryptographic services through Windows APIs. .NET exposes cryptographically secure random-number generation through its RandomNumberGenerator API.

All three mechanisms are designed for cryptographic use when accessed and configured correctly. Their implementations differ, but the statistical measurements in this experiment do not establish that one mechanism is more secure than another.

9. Why Statistical Tests Do Not Guarantee Cryptographic Security

Statistical tests examine observable properties of generated data, such as frequency balance, repeated patterns, and correlation.

A generator can produce statistically convincing output while still being predictable to an attacker who knows its internal state or can exploit an implementation weakness.

Cryptographic security also depends on secure initialization, internal state management, resistance to prediction, correct implementation, and protection of secret material.

Therefore, passing statistical tests is useful evidence about selected properties of a sample, but it is not proof of cryptographic security.

10. Result

Random data was successfully analysed from Linux /dev/urandom, OpenSSL rand, and Windows CNG through .NET. The byte-frequency p-values exceeded 0.05, the proportions of one bits were close to 50%, and the measured lag-1 correlations were close to zero.

The OpenSSL runs result and repeated-adjacent-pairs calculation require further verification. The experiment demonstrates that statistical testing can identify selected characteristics of random data but cannot independently establish cryptographic security.

11. Precautions
Use raw binary output rather than hexadecimal text for analysis.
Verify that each dataset contains at least 1 MiB.
Ensure that each file was generated using the intended random-number mechanism.
Use appropriate statistical tests and significance levels.
Verify unexpected results and calculations before drawing conclusions.
Do not treat high p-values or near-zero correlations as proof of cryptographic security.
12. References
Linux manual page: random(4).
OpenSSL documentation: Random-number generation and openssl rand.
Microsoft .NET documentation: System.Security.Cryptography.RandomNumberGenerator.
NIST SP 800-22, A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications.

Before submission: Verify the repeated-adjacent-pairs calculation and the OpenSSL runs-test implementation. These are the two measurements in your actual output that deserve additional investigation.
