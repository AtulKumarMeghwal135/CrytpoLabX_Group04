"""
Main Driver
-----------
Runs Shift Cipher encryption/decryption,
Dictionary Scoring attack and Chi-Square attack.
"""

import os

from shift_cipher import encrypt, decrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


def main():
    print("=" * 60)
    print("        SHIFT CIPHER CRYPTANALYSIS")
    print("=" * 60)

    plaintext = input("\nEnter plaintext: ")
    actual_key = int(input("Enter encryption key (0-25): "))

    # Encrypt the plaintext
    ciphertext = encrypt(plaintext, actual_key)

    print("\n" + "-" * 60)
    print("ENCRYPTION")
    print("-" * 60)

    print(f"Plaintext   : {plaintext}")
    print(f"Actual Key  : {actual_key}")
    print(f"Ciphertext  : {ciphertext}")

    # Dictionary file
    dictionary_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "dictionary",
        "english_words.txt"
    )

    # Dictionary attack
    print("\n" + "-" * 60)
    print("DICTIONARY SCORING ATTACK")
    print("-" * 60)

    try:
        dictionary_key, dictionary_plaintext, dictionary_score_value = (
            dictionary_attack(ciphertext, dictionary_path)
        )

        print(f"Predicted Key : {dictionary_key}")
        print(f"Score         : {dictionary_score_value}")
        print(f"Plaintext     : {dictionary_plaintext}")

    except FileNotFoundError as error:
        print(error)
        dictionary_key = None

    # Chi-Square attack
    print("\n" + "-" * 60)
    print("CHI-SQUARE ATTACK")
    print("-" * 60)

    chi_key, chi_plaintext, chi_score = chi_square_attack(ciphertext)

    print(f"Predicted Key : {chi_key}")
    print(f"Chi-Square    : {chi_score:.4f}")
    print(f"Plaintext     : {chi_plaintext}")

    # Comparison
    print("\n" + "=" * 60)
    print("              FINAL COMPARISON")
    print("=" * 60)

    print(f"Actual Key       : {actual_key}")

    if dictionary_key is not None:
        print(f"Dictionary Key   : {dictionary_key}")
        print(
            f"Dictionary Correct? : "
            f"{'YES' if dictionary_key == actual_key else 'NO'}"
        )
    else:
        print("Dictionary Key   : Not available")

    print(f"Chi-Square Key   : {chi_key}")
    print(
        f"Chi-Square Correct? : "
        f"{'YES' if chi_key == actual_key else 'NO'}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
