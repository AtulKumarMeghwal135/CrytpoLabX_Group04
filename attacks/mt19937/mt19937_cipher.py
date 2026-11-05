import random
import secrets
import string
import time


# ==========================================
# MT19937 STREAM CIPHER
# ==========================================

def stream_cipher(data, seed):

    rng = random.Random(seed)

    result = bytearray()

    for byte in data:
        key_byte = rng.getrandbits(8)
        result.append(byte ^ key_byte)

    return bytes(result)


# ==========================================
# BASIC ENCRYPTION AND DECRYPTION
# ==========================================

print("\n========== ENCRYPTION TEST ==========")

message = b"Hello MT19937 Stream Cipher"

seed = 12345

ciphertext = stream_cipher(message, seed)

decrypted = stream_cipher(ciphertext, seed)

print("Original Message :", message.decode())
print("Seed             :", seed)
print("Ciphertext       :", ciphertext.hex())
print("Decrypted Message:", decrypted.decode())

assert decrypted == message

print("Encryption/Decryption: SUCCESS")


# ==========================================
# GENERATE KNOWN PLAINTEXT
# ==========================================

print("\n========== PLAINTEXT GENERATION ==========")

prefix_length = secrets.randbelow(16) + 5

characters = string.ascii_letters + string.digits + string.punctuation

prefix = ''.join(
    secrets.choice(characters)
    for _ in range(prefix_length)
)

plaintext = (prefix + "A" * 14).encode()

original_seed = secrets.randbelow(65536)

ciphertext = stream_cipher(plaintext, original_seed)

print("Original Seed     :", original_seed)
print("Prefix Length     :", prefix_length)
print("Original Plaintext:", plaintext.decode())
print("Ciphertext        :", ciphertext.hex())


# ==========================================
# BRUTE FORCE SEED RECOVERY
# ==========================================

print("\n========== SEED RECOVERY ==========")

recovered_seed = None
recovered_plaintext = None

candidates_tested = 0

start = time.time()

for candidate_seed in range(65536):

    candidates_tested += 1

    decrypted_text = stream_cipher(ciphertext, candidate_seed)

    if b"A" * 14 in decrypted_text:

        recovered_seed = candidate_seed
        recovered_plaintext = decrypted_text

        break

end = time.time()


# ==========================================
# VERIFICATION
# ==========================================

print("\n========== ATTACK RESULTS ==========")

print("Candidates Tested :", candidates_tested)
print("Time Taken        :", round(end - start, 6), "seconds")

print("Original Seed     :", original_seed)
print("Recovered Seed    :", recovered_seed)

print("Recovered Plaintext:",
      recovered_plaintext.decode() if recovered_plaintext else None)

print("Seed Correct:",
      recovered_seed == original_seed)

print("Plaintext Correct:",
      recovered_plaintext == plaintext)

assert recovered_seed == original_seed
assert recovered_plaintext == plaintext

print("\nPART A COMPLETED SUCCESSFULLY!")
