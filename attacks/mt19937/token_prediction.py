import random
import time


# ==========================================
# TOKEN GENERATION
# ==========================================

print("\n========== TOKEN GENERATION ==========")

# Current Unix timestamp
timestamp = int(time.time())

# Initialize MT19937
rng = random.Random(timestamp)

# Generate 16-byte token
token_bytes = bytes(
    rng.getrandbits(8) for _ in range(16)
)

observed_token = token_bytes.hex()

print("Original Timestamp:", timestamp)
print("Generated Token   :", observed_token)
print("Token Length      :", len(token_bytes), "bytes")


# ==========================================
# ATTACKER SEARCH INTERVAL
# ==========================================

print("\n========== SEARCH INTERVAL ==========")

# Simulate an attacker's approximate clock estimate.
# The estimate is deliberately different from the true timestamp.
estimated_timestamp = timestamp + 30

start_timestamp = estimated_timestamp - 300
end_timestamp = estimated_timestamp + 300

print("Estimated Timestamp:", estimated_timestamp)
print("Start Timestamp    :", start_timestamp)
print("End Timestamp      :", end_timestamp)

print("Total Candidates   :",
      end_timestamp - start_timestamp + 1)


# ==========================================
# TIMESTAMP PREDICTION ATTACK
# ==========================================

print("\n========== TIMESTAMP RECOVERY ==========")

recovered_timestamp = None
recovered_token = None

candidates_tested = 0

attack_start = time.time()

for candidate_time in range(start_timestamp, end_timestamp + 1):

    candidates_tested += 1

    rng = random.Random(candidate_time)

    candidate_token = bytes(
        rng.getrandbits(8) for _ in range(16)
    )

    if candidate_token.hex() == observed_token:

        recovered_timestamp = candidate_time
        recovered_token = candidate_token

        break

attack_end = time.time()


# ==========================================
# VERIFICATION
# ==========================================

print("\n========== ATTACK RESULTS ==========")

print("Candidates Tested  :", candidates_tested)

print("Time Taken         :",
      round(attack_end - attack_start, 6), "seconds")

print("Recovered Timestamp:", recovered_timestamp)

print("Recovered Token    :",
      recovered_token.hex() if recovered_token else None)


# Regenerate token using recovered timestamp

print("\n========== TOKEN VERIFICATION ==========")

if recovered_timestamp is not None:

    verification_rng = random.Random(recovered_timestamp)

    verification_token = bytes(
        verification_rng.getrandbits(8)
        for _ in range(16)
    )

    print("Original Timestamp :", timestamp)

    print("Recovered Timestamp:", recovered_timestamp)

    print("Original Token     :", observed_token)

    print("Regenerated Token  :", verification_token.hex())

    print("Timestamp Correct  :", recovered_timestamp == timestamp)

    print("Token Matches      :", verification_token.hex() == observed_token)

    assert recovered_timestamp == timestamp
    assert verification_token.hex() == observed_token

    print("\nPART B COMPLETED SUCCESSFULLY!")

else:

    print("No matching timestamp found.")
