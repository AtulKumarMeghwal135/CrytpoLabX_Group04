# Padding Oracle Attack on AES-CBC

## Objective

Demonstrate how a Padding Oracle Attack can recover plaintext
from an AES-CBC encrypted message without knowing the AES key.

## Concepts

AES-CBC encryption uses:

C_i = AES_K(P_i XOR C_(i-1))

During decryption:

P_i = AES_K^(-1)(C_i) XOR C_(i-1)

where C_0 is the IV.

The attack exploits the fact that modifying the previous ciphertext
block changes the plaintext of the target block.

## PKCS#7 Padding

AES has a block size of 16 bytes.

PKCS#7 adds padding so that the plaintext length becomes a multiple
of 16 bytes.

For example, if 3 bytes of padding are required:

03 03 03

## Padding Oracle

The oracle decrypts a ciphertext and reports whether the resulting
plaintext has valid PKCS#7 padding.

The attacker does not know or access the AES key.

The attacker only receives:

- IV
- ciphertext
- valid/invalid padding response

## Attack

For each ciphertext block, bytes are recovered from right to left.

The attacker modifies the previous ciphertext block so that the
decrypted target block ends with:

01
02 02
03 03 03
...
10 10 ... 10

A valid padding response provides information about the intermediate
AES decryption value.

The plaintext is then calculated using:

P_i = I_i XOR C_(i-1)

where:

I_i = AES_K^(-1)(C_i)

## Query Count

The program counts every call made to the padding oracle.

The exact number of queries depends on the ciphertext and the
guesses required for each plaintext byte.

## Security Recommendation

A real system should not expose a distinguishable padding-validation
oracle.

Applications should use authenticated encryption such as AES-GCM
or another secure AEAD mode.

If CBC must be used, authentication should be performed correctly
and error responses should not reveal whether padding validation
succeeded.

## Files

- `src/padding_oracle_attack.py`
  - AES-CBC encryption
  - PKCS#7 padding
  - Padding oracle
  - Padding Oracle Attack

- `outputs/recovered_plaintext.txt`
  - Recovered plaintext

- `outputs/oracle_queries.txt`
  - Total number of oracle queries
