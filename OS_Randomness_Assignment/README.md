# Evaluation of Operating-System Random Number Generators

## 1. Objective

The objective of this assignment is to evaluate operating-system random-number generation mechanisms and investigate their suitability for cryptographic applications.

The experiment compares cryptographically secure random-number generators provided by Linux, OpenSSL, and Windows.

## 2. Random Number Generation Mechanisms

The following mechanisms are investigated:

1. **Linux `/dev/urandom`:** Provides cryptographically secure random bytes through the Linux kernel random-number generator.
2. **OpenSSL `rand`:** Generates cryptographically secure pseudorandom bytes using OpenSSL's random-number generation facilities.
3. **Windows CNG / .NET:** Provides cryptographically secure random bytes through Windows cryptographic APIs.

## 3. Tools and Technologies

- Ubuntu Linux
- Windows
- Python 3
- Jupyter Notebook
- NumPy
- Matplotlib
- SciPy
- Pandas
- OpenSSL

## 4. Methodology

### Step 1: Random Data Generation

Generate at least 1 MB of random data using each mechanism.

Linux:

```bash
head -c 1048576 /dev/urandom > linux_random.bin
```

OpenSSL:

```bash
openssl rand -out openssl_random.bin 1048576
```

Windows:

Use the Windows CNG API or the .NET `RandomNumberGenerator` class to generate random bytes.

### Step 2: Statistical Analysis

Analyze the generated data using the following techniques:

**Byte-Frequency Distribution**

Examine the frequency of all 256 possible byte values to identify distribution biases.

**Bit Distribution**

Calculate the proportions of zeros and ones. Ideally, each should occur approximately 50% of the time.

**Repeated-Pattern Analysis**

Examine repeated byte sequences and compare their frequencies with expected random behavior.

**Serial Correlation**

Measure the linear relationship between consecutive bytes. Ideally, serial correlation should be close to zero.

### Step 3: Statistical Tests

The analysis includes appropriate statistical tests, such as:

- Chi-square goodness-of-fit test
- Monobit frequency test
- Runs test

The tests help determine whether the generated data exhibits statistically significant deviations from ideal random behavior.

## 5. Comparison of Random Number Generators

| Feature | Linux /dev/urandom | OpenSSL rand | Windows CNG/.NET |
|---|---|---|---|
| Platform | Linux | Cross-platform | Windows |
| Generator | Kernel CSPRNG | OpenSSL CSPRNG | Windows cryptographic RNG |
| Cryptographic Use | Yes | Yes | Yes |
| Entropy Source | Kernel-managed sources | Typically operating-system sources | Windows-managed sources |
| Random Data Generation | Supported | Supported | Supported |

## 6. Cryptographic Security

Passing statistical tests does not guarantee cryptographic security.

A generator can produce statistically uniform sequences while remaining predictable if its internal state or seed is known.

Cryptographically secure random-number generators must provide computational unpredictability and use appropriate seeding and state-management mechanisms.

## 7. Conclusion

This assignment studies the behavior of random-number generators used in cryptographic applications.

Byte-frequency analysis, bit-distribution analysis, repeated-pattern analysis, serial correlation, and statistical tests provide methods for examining the properties of generated random data.

Linux, OpenSSL, and Windows provide random-number generation mechanisms intended for cryptographic applications.

However, statistical testing alone cannot establish cryptographic security. Secure algorithm design, sufficient entropy, correct initialization, and resistance to prediction are also necessary.

## 8. References

1. Linux random-number generation documentation: https://man7.org/linux/man-pages/man7/random.7.html
2. OpenSSL documentation: https://docs.openssl.org/
3. Microsoft cryptographic API documentation: https://learn.microsoft.com/
4. NIST SP 800-22: Statistical Test Suite for Random and Pseudorandom Number Generators.
