from collections import Counter, defaultdict


# ============================================================
# VIGENERE CIPHER - CIPHERTEXT ONLY ATTACK
# GROUP 4 (EVEN) -> CIPHERTEXT 2
# ============================================================


# ------------------------------------------------------------
# 1. CLEAN CIPHERTEXT
# ------------------------------------------------------------

def clean_ciphertext(ciphertext):
    """
    Remove spaces, numbers and special characters.
    Convert all letters to uppercase.
    """
    return ''.join(
        ch for ch in ciphertext.upper()
        if ch.isalpha()
    )


# ------------------------------------------------------------
# 2. FIND REPEATED PATTERNS
# ------------------------------------------------------------

def find_repeated_patterns(ciphertext, min_length=3, max_length=5):
    """
    Find repeated sequences in the ciphertext.

    Returns:
        {
            pattern: [position1, position2, ...]
        }
    """

    patterns = defaultdict(list)

    for length in range(min_length, max_length + 1):

        for i in range(len(ciphertext) - length + 1):

            pattern = ciphertext[i:i + length]

            patterns[pattern].append(i)

    # Keep only repeated patterns
    repeated = {}

    for pattern, positions in patterns.items():

        if len(positions) > 1:
            repeated[pattern] = positions

    return repeated


# ------------------------------------------------------------
# 3. CALCULATE DISTANCES
# ------------------------------------------------------------

def calculate_distances(repeated_patterns):
    """
    Calculate distances between repeated occurrences.

    Returns:
        [(pattern, distance), ...]
    """

    distances = []

    for pattern, positions in repeated_patterns.items():

        for i in range(len(positions) - 1):

            distance = positions[i + 1] - positions[i]

            distances.append(
                (pattern, distance)
            )

    return distances


# ------------------------------------------------------------
# 4. FIND FACTORS
# ------------------------------------------------------------

def find_factors(distance, max_factor=20):
    """
    Find possible key lengths from a distance.
    """

    factors = []

    for i in range(2, min(distance, max_factor) + 1):

        if distance % i == 0:
            factors.append(i)

    return factors


# ------------------------------------------------------------
# 5. KASISKI ANALYSIS
# ------------------------------------------------------------

def kasiski_analysis(ciphertext, max_key_length=20):
    """
    Perform Kasiski examination.

    Repeated patterns -> distances -> factors
    -> possible key lengths.
    """

    repeated = find_repeated_patterns(ciphertext)

    distances = calculate_distances(repeated)

    factor_counts = Counter()

    for pattern, distance in distances:

        factors = find_factors(
            distance,
            max_key_length
        )

        for factor in factors:

            factor_counts[factor] += 1

    candidates = factor_counts.most_common()

    return candidates, repeated, distances


# ------------------------------------------------------------
# 6. INDEX OF COINCIDENCE
# ------------------------------------------------------------

def calculate_ic(text):
    """
    Calculate Index of Coincidence.

    IC = sum(fi(fi-1)) / N(N-1)
    """

    n = len(text)

    if n <= 1:
        return 0.0

    counts = Counter(text)

    numerator = 0

    for count in counts.values():

        numerator += count * (count - 1)

    denominator = n * (n - 1)

    return numerator / denominator


# ------------------------------------------------------------
# 7. SPLIT INTO GROUPS
# ------------------------------------------------------------

def split_into_groups(ciphertext, key_length):
    """
    Divide ciphertext according to key position.

    For key length 3:

    Group 1 -> positions 0,3,6,...
    Group 2 -> positions 1,4,7,...
    Group 3 -> positions 2,5,8,...
    """

    groups = []

    for i in range(key_length):

        group = ciphertext[i::key_length]

        groups.append(group)

    return groups


# ------------------------------------------------------------
# 8. FREQUENCY ANALYSIS
# ------------------------------------------------------------

def frequency_analysis(group):
    """
    Calculate A-Z frequency for one group.
    """

    counts = Counter(group)

    frequencies = {}

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        frequencies[letter] = counts.get(
            letter,
            0
        )

    return frequencies


# ------------------------------------------------------------
# ENGLISH LETTER FREQUENCIES
# ------------------------------------------------------------

ENGLISH_FREQUENCIES = {

    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02360,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}


# ------------------------------------------------------------
# 9. FIND SHIFT
# ------------------------------------------------------------

def find_shift(group):
    """
    Find the most likely Caesar shift for a group.

    Chi-square frequency analysis is used.

    Returns:
        shift
        chi-square score
    """

    n = len(group)

    if n == 0:
        return 0, float("inf")

    best_shift = 0
    best_score = float("inf")

    # Try every possible Caesar shift
    for shift in range(26):

        decrypted = ""

        for char in group:

            value = (
                ord(char) -
                ord('A') -
                shift
            ) % 26

            decrypted += chr(
                value + ord('A')
            )

        counts = Counter(decrypted)

        chi_square = 0.0

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            observed = counts.get(
                letter,
                0
            )

            expected = (
                ENGLISH_FREQUENCIES[letter]
                * n
            )

            if expected > 0:

                chi_square += (
                    (observed - expected) ** 2
                ) / expected

        if chi_square < best_score:

            best_score = chi_square
            best_shift = shift

    return best_shift, best_score


# ------------------------------------------------------------
# 10. FIND KEY
# ------------------------------------------------------------

def find_key(groups):
    """
    Find the probable Vigenere key.

    Each group corresponds to one key letter.
    """

    key = ""

    shift_information = []

    for group in groups:

        shift, score = find_shift(group)

        key_letter = chr(
            ord('A') + shift
        )

        key += key_letter

        shift_information.append(
            (shift, score)
        )

    return key, shift_information


# ------------------------------------------------------------
# 11. VIGENERE DECRYPT
# ------------------------------------------------------------

def vigenere_decrypt(ciphertext, key):
    """
    Decrypt ciphertext using recovered key.
    """

    plaintext = ""

    for i, char in enumerate(ciphertext):

        cipher_value = (
            ord(char) - ord('A')
        )

        key_value = (
            ord(key[i % len(key)]) -
            ord('A')
        )

        plain_value = (
            cipher_value - key_value
        ) % 26

        plaintext += chr(
            plain_value + ord('A')
        )

    return plaintext


# ------------------------------------------------------------
# 12. VIGENERE ENCRYPT
# ------------------------------------------------------------

def vigenere_encrypt(plaintext, key):
    """
    Encrypt plaintext using Vigenere key.
    """

    ciphertext = ""

    for i, char in enumerate(plaintext):

        plain_value = (
            ord(char) - ord('A')
        )

        key_value = (
            ord(key[i % len(key)]) -
            ord('A')
        )

        cipher_value = (
            plain_value + key_value
        ) % 26

        ciphertext += chr(
            cipher_value + ord('A')
        )

    return ciphertext


# ------------------------------------------------------------
# 13. VERIFY
# ------------------------------------------------------------

def verify(ciphertext, plaintext, key):
    """
    Re-encrypt plaintext and compare it
    with the original ciphertext.
    """

    encrypted = vigenere_encrypt(
        plaintext,
        key
    )

    return encrypted == ciphertext


# ------------------------------------------------------------
# HELPER: RANK KEY LENGTHS USING IC
# ------------------------------------------------------------

def rank_key_lengths(ciphertext, kasiski_candidates,
                     max_key_length=20):
    """
    Use average IC to help determine the
    probable key length.
    """

    kasiski_lengths = set()

    for length, count in kasiski_candidates:

        kasiski_lengths.add(length)

    results = []

    for key_length in range(
        2,
        max_key_length + 1
    ):

        groups = split_into_groups(
            ciphertext,
            key_length
        )

        ics = []

        for group in groups:

            ics.append(
                calculate_ic(group)
            )

        average_ic = (
            sum(ics) / len(ics)
        )

        # English plaintext IC is approximately 0.066
        difference = abs(
            average_ic - 0.066
        )

        # Give a small advantage to lengths
        # supported by Kasiski.
        if key_length in kasiski_lengths:

            score = difference - 0.005

        else:

            score = difference

        results.append(
            (
                key_length,
                average_ic,
                score
            )
        )

    results.sort(
        key=lambda x: x[2]
    )

    return results


# ------------------------------------------------------------
# DISPLAY FREQUENCY TABLE
# ------------------------------------------------------------

def display_frequency_table(groups):

    for number, group in enumerate(
        groups,
        start=1
    ):

        frequencies = frequency_analysis(
            group
        )

        print()
        print("-" * 75)

        print(
            "GROUP",
            number
        )

        print("-" * 75)

        print(
            "Group text:",
            group
        )

        print()
        print(
            "Letter :",
            end=" "
        )

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            print(
                f"{letter:>3}",
                end=" "
            )

        print()

        print(
            "Count  :",
            end=" "
        )

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            print(
                f"{frequencies[letter]:>3}",
                end=" "
            )

        print()

        print()
        print("Percentage:")

        total = len(group)

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            percentage = (
                frequencies[letter]
                / total
                * 100
            )

            print(
                f"{letter} = {percentage:6.2f}%",
                end="    "
            )

        print()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # ========================================================
    # CIPHERTEXT 2 - EVEN GROUP
    # ========================================================

    ciphertext2 = """

    QRBAI UWYOK ILBRZ XTUWL EGXSN VDXWR XMHXY FCGMW
    WWSME LSXUZ

    MKMFS BNZIF YEIEG RFZRX WKUFA XQEDX DTTHY NTBRJ
    LHTAI KOCZX

    QHBND ZIGZG PXARJ EDYSJ NUMKI FLBTN HWISW NVLFM
    EGXAI AAWSL

    FMHXR SGRIG HEQTU MLGLV BRSIL AEZSG XCMHT OWHFM
    LWMRK HPRFB

    ELWGF RUGPB HNBEM KBNVW HHUEA KILBN BMLHK XUGML
    YQKHP RFBEL

    EJYNV WSIJB GAXGO TPMXR TXFKI WUALB RGWIE GHWHG
    AMEWW LTAEL

    NUMRE UWTBL SDPRL YVRET LEEDF ROBEQ UXTHX ZYOZB
    XLKAC KSOHN

    VWXKS MAEPH IYQMM FSECH RFYPB BSQTX TPIWH GPXQD
    FWTAI KNNBX

    SIYKE TXTLV BTMQA LAGHG OTPMX RTXTH XSFYG WMVKH
    LOIVU ALMLD

    LTSYV WYNVW MQVXP XRVYA BLXDL XSMLW SUIOI IMELI
    SOYEB HPHNR

    WTVUI AKEYG WIETG WWBVM VDUMA EPAUA KXWHK MAUPA
    MUKHQ PWKCX

    EFXGW WSDDE OMLWL NKMWD FWTAM FAFEA MFZBN WIHYA
    LXRWK MAMIK

    GNGHJ UAZHM HGUAL YSULA ELYHJ BZMSI LAILH WWYIK
    EWAHN PMLBN

    NBVPJ XLBEF WRWGX KWIRH XWWGQ HRRXW IOMFY CZHZL
    VXNVI OYZCM

    YDDEY IPWXT MMSHS VHHXZ YEWNV OAOEL SMLSW KXXFX
    STRVI HZLEF

    JXDAS FIE

    """

    # ========================================================
    # STEP 1 - PREPROCESSING
    # ========================================================

    ciphertext = clean_ciphertext(
        ciphertext2
    )

    print()
    print("=" * 80)
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("CIPHERTEXT-ONLY ATTACK")
    print("GROUP NUMBER: 4 (EVEN)")
    print("=" * 80)

    print()
    print("STEP 1: PREPROCESSING")
    print("-" * 80)

    print(
        "Clean ciphertext length:",
        len(ciphertext)
    )

    print()
    print("Clean ciphertext:")

    print(ciphertext)

    # ========================================================
    # STEP 2 - KASISKI
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 2: KASISKI EXAMINATION")
    print("=" * 80)

    candidates, repeated, distances = (
        kasiski_analysis(
            ciphertext,
            max_key_length=20
        )
    )

    print()
    print("Repeated patterns:")

    if len(repeated) == 0:

        print("No repeated patterns found.")

    else:

        count = 0

        for pattern, positions in repeated.items():

            print(
                f"{pattern} -> {positions}"
            )

            count += 1

            # Avoid printing hundreds of patterns
            if count >= 30:
                break

    print()
    print("Distances between repeated patterns:")

    if len(distances) == 0:

        print("No distances found.")

    else:

        for pattern, distance in distances[:50]:

            print(
                f"Pattern: {pattern:5s}"
                f"  Distance: {distance}"
            )

    print()
    print("Kasiski candidate key lengths:")

    if len(candidates) == 0:

        print(
            "No strong candidates found."
        )

    else:

        for length, count in candidates:

            print(
                f"Key Length = {length:2d}"
                f"   Factor Count = {count}"
            )

    # ========================================================
    # STEP 3 - IC ANALYSIS
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 3: INDEX OF COINCIDENCE")
    print("=" * 80)

    ic_results = rank_key_lengths(
        ciphertext,
        candidates,
        max_key_length=20
    )

    print()
    print(
        "Length       Average IC        Score"
    )

    print("-" * 50)

    for length, average_ic, score in ic_results:

        print(
            f"{length:5d}"
            f"       {average_ic:.5f}"
            f"       {score:.5f}"
        )

    # ========================================================
    # ESTIMATE KEY LENGTH
    # ========================================================

    estimated_key_length = (
        ic_results[0][0]
    )

    print()
    print(
        "Estimated Key Length =",
        estimated_key_length
    )

    # ========================================================
    # STEP 4 - SPLIT INTO GROUPS
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 4: SPLITTING CIPHERTEXT INTO GROUPS")
    print("=" * 80)

    groups = split_into_groups(
        ciphertext,
        estimated_key_length
    )

    for number, group in enumerate(
        groups,
        start=1
    ):

        print(
            f"Group {number}: {group}"
        )

    # ========================================================
    # STEP 5 - FREQUENCY ANALYSIS
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 5: FREQUENCY ANALYSIS")
    print("=" * 80)

    display_frequency_table(
        groups
    )

    # ========================================================
    # STEP 6 - FIND KEY
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 6: RECOVERING PROBABLE KEY")
    print("=" * 80)

    key, shift_information = find_key(
        groups
    )

    print()
    print(
        "Group     Shift     Key Letter"
    )

    print("-" * 40)

    for number, (shift, score) in enumerate(
        shift_information,
        start=1
    ):

        key_letter = chr(
            ord('A') + shift
        )

        print(
            f"{number:5d}"
            f"{shift:10d}"
            f"{key_letter:^15s}"
        )

    print()
    print(
        "Recovered Key =",
        key
    )

    # ========================================================
    # STEP 7 - DECRYPTION
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 7: VIGENERE DECRYPTION")
    print("=" * 80)

    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print()
    print("Recovered Plaintext:")
    print()

    # Print plaintext in groups of 80 characters
    for i in range(
        0,
        len(plaintext),
        80
    ):

        print(
            plaintext[i:i + 80]
        )

    # ========================================================
    # STEP 8 - VERIFICATION
    # ========================================================

    print()
    print("=" * 80)
    print("STEP 8: VERIFICATION")
    print("=" * 80)

    re_encrypted = vigenere_encrypt(
        plaintext,
        key
    )

    result = verify(
        ciphertext,
        plaintext,
        key
    )

    print()
    print(
        "Re-encrypted ciphertext:"
    )

    print(re_encrypted)

    print()
    print(
        "Original ciphertext:"
    )

    print(ciphertext)

    print()
    print(
        "Verification:"
    )

    if result:

        print(
            "SUCCESS!"
        )

        print(
            "The re-encrypted plaintext"
            " exactly matches the original"
            " ciphertext."
        )

    else:

        print(
            "FAILED!"
        )

        print(
            "The re-encrypted ciphertext"
            " does not match the original."
        )

    print()
    print("=" * 80)
    print("ATTACK COMPLETED")
    print("=" * 80)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()

