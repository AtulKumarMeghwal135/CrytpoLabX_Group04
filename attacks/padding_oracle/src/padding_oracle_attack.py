from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


BLOCK_SIZE = 16


# ============================================================
# PKCS#7 PADDING
# ============================================================

def pkcs7_pad(data):
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    padding = bytes([padding_length]) * padding_length
    return data + padding


def pkcs7_unpad(data):
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padded data")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]


# ============================================================
# AES-CBC ENCRYPTION
# ============================================================

def aes_cbc_encrypt(key, iv, plaintext):
    padded_plaintext = pkcs7_pad(plaintext)

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    return encryptor.update(padded_plaintext) + encryptor.finalize()


# ============================================================
# PADDING ORACLE
# ============================================================

class PaddingOracle:
    """
    The oracle knows the AES key.

    The attacker never receives the key.
    The attacker can only call check_padding().
    """

    def __init__(self, key):
        self._key = key
        self.query_count = 0

    def check_padding(self, iv, ciphertext):
        """
        Return True if the decrypted ciphertext has
        valid PKCS#7 padding, otherwise False.
        """

        self.query_count += 1

        try:
            cipher = Cipher(
                algorithms.AES(self._key),
                modes.CBC(iv),
                backend=default_backend()
            )

            decryptor = cipher.decryptor()

            plaintext = decryptor.update(ciphertext)
            plaintext += decryptor.finalize()

            pkcs7_unpad(plaintext)

            return True

        except ValueError:
            return False


# ============================================================
# PADDING ORACLE ATTACK
# ============================================================

def recover_block(oracle, previous_block, target_block):
    """
    Recover one plaintext block.

    The attacker only receives:
        1. previous ciphertext block
        2. target ciphertext block
        3. oracle access

    The AES key is NOT used here.
    """

    intermediate = bytearray(BLOCK_SIZE)
    recovered_plaintext = bytearray(BLOCK_SIZE)

    modified_block = bytearray(previous_block)

    # Recover bytes from right to left.
    for padding_value in range(1, BLOCK_SIZE + 1):

        byte_index = BLOCK_SIZE - padding_value

        # Force already recovered bytes to contain
        # the desired padding value.
        for j in range(byte_index + 1, BLOCK_SIZE):
            modified_block[j] = (
                intermediate[j] ^ padding_value
            )

        found = False

        for guess in range(256):

            modified_block[byte_index] = guess

            valid = oracle.check_padding(
                bytes(modified_block),
                target_block
            )

            if valid:

                # For padding = 1, verify the result by
                # modifying another byte. This helps avoid
                # accidental valid-padding cases.
                if padding_value == 1 and byte_index > 0:

                    test_block = bytearray(modified_block)
                    test_block[byte_index - 1] ^= 1

                    if not oracle.check_padding(
                        bytes(test_block),
                        target_block
                    ):
                        continue

                intermediate[byte_index] = (
                    guess ^ padding_value
                )

                recovered_plaintext[byte_index] = (
                    intermediate[byte_index]
                    ^ previous_block[byte_index]
                )

                found = True
                break

        if not found:
            raise RuntimeError(
                f"Could not recover byte {byte_index}"
            )

    return bytes(recovered_plaintext)


def padding_oracle_attack(oracle, iv, ciphertext):
    """
    Recover the complete plaintext.

    The attack receives only:
        - IV
        - ciphertext
        - padding oracle

    The AES key is never passed to this function.
    """

    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length must be a multiple of 16")

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered = b""

    previous_block = iv

    print("\nStarting Padding Oracle Attack...")
    print("----------------------------------------")

    for block_number, target_block in enumerate(blocks, start=1):

        print(f"Recovering block {block_number}/{len(blocks)}...")

        plaintext_block = recover_block(
            oracle,
            previous_block,
            target_block
        )

        recovered += plaintext_block

        print(
            "Recovered block:",
            repr(plaintext_block)
        )

        previous_block = target_block

    # Remove PKCS#7 padding after all blocks are recovered.
    return pkcs7_unpad(recovered)


# ============================================================
# MAIN DEMONSTRATION
# ============================================================

def main():

    print("=" * 60)
    print("             AES-CBC PADDING ORACLE ATTACK")
    print("=" * 60)

    # --------------------------------------------------------
    # Encryption side
    # --------------------------------------------------------

    plaintext = (
        b"Padding oracle attacks exploit the difference between "
        b"valid and invalid PKCS7 padding. AES itself remains "
        b"secure, but a vulnerable CBC implementation can leak "
        b"plaintext through its padding validation response."
    )

    # Generate a random AES-128 key.
    key = os.urandom(16)

    # Generate a random IV.
    iv = os.urandom(16)

    ciphertext = aes_cbc_encrypt(
        key,
        iv,
        plaintext
    )

    print("\nOriginal plaintext:")
    print(plaintext.decode())

    print("\nIV:")
    print(iv.hex())

    print("\nCiphertext:")
    print(ciphertext.hex())

    # --------------------------------------------------------
    # Create oracle.
    #
    # The oracle knows the key.
    # The attack does NOT.
    # --------------------------------------------------------

    oracle = PaddingOracle(key)

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Only IV, ciphertext and oracle are given to the attack.
    # The key is NOT passed to padding_oracle_attack().
    # --------------------------------------------------------

    recovered_plaintext = padding_oracle_attack(
        oracle,
        iv,
        ciphertext
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                    ATTACK RESULTS")
    print("=" * 60)

    print("\nRecovered plaintext:")
    print(recovered_plaintext.decode())

    print("\nTotal oracle queries:")
    print(oracle.query_count)

    print("\nPlaintext successfully recovered:")
    print(recovered_plaintext == plaintext)

    # Save recovered plaintext.
    os.makedirs("outputs", exist_ok=True)

    with open(
        "outputs/recovered_plaintext.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(recovered_plaintext.decode())

    # Save query count.
    with open(
        "outputs/oracle_queries.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(str(oracle.query_count))

    print("\nOutput files created:")
    print("outputs/recovered_plaintext.txt")
    print("outputs/oracle_queries.txt")


if __name__ == "__main__":
    main()
