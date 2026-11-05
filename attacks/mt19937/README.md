# MT19937 Insecurity Demonstration

## Objective
To demonstrate why the MT19937 pseudo-random number generator is unsuitable for cryptographic applications.

## Assignment Tasks

### Part A: Known Plaintext Attack
- Implemented a toy stream cipher using MT19937.
- Generated a plaintext containing a random printable prefix followed by 14 consecutive `A` characters.
- Encrypted the plaintext using a randomly selected 16-bit seed.
- Brute-forced the possible seeds from 0 to 65535.
- Recovered the correct seed and original plaintext.

### Part B: Timestamp-Based Token Prediction
- Generated a 16-byte token using MT19937 seeded with the current Unix timestamp.
- Simulated an attacker searching a timestamp interval of ±300 seconds.
- Recovered the timestamp by generating and comparing candidate tokens.
- Verified the recovered timestamp by regenerating the token.

## Files

| File | Description |
|---|---|
| `MT19937_Assignment.ipynb` | Complete explanation, implementation, and results |
| `mt19937_cipher.py` | Part A: stream cipher and known plaintext attack |
| `token_prediction.py` | Part B: timestamp-based token prediction |

## How to Run

Activate the virtual environment if one is being used:

```bash
source myenv/bin/activate
```

Run Part A:

```bash
python3 mt19937_cipher.py
```

Run Part B:

```bash
python3 token_prediction.py
```

Open the notebook:

```bash
jupyter notebook MT19937_Assignment.ipynb
```

## Conclusion

MT19937 is designed for statistical randomness and simulations, not cryptographic security. Its predictable output and deterministic seeding make it vulnerable to attacks when used for encryption or security tokens.

Cryptographic applications should use a cryptographically secure random number generator (CSPRNG), such as Python's `secrets` module or the operating system's secure random source.
