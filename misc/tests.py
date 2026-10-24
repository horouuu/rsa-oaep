from lib.oaep import pad_oaep
from lib.oaep import unpad_oaep

def print_separator():
    print("------------------------------------------")

def test_oaep_correctness():
    print_separator()
    print('Running EME-OAEP with message "HELLO"')
    inp = bytes("HELLO", 'utf-8')
    padded = pad_oaep(inp, 256)
    print('Padded: ', padded)
    decoded = unpad_oaep(padded).decode('utf-8')
    print('Decoded: ', decoded)

    if (decoded != "HELLO"):
        raise AssertionError('Decoded message does not equal "HELLO"')
    print("SUCCESS: Correctness")
    print_separator()

def test_oaep_randomness():
    print_separator()
    print('Running EME-OAEP twice with message "Konchikuwa"')
    inp = bytes("Konchikuwa", 'utf-8')
    padded_1 = pad_oaep(inp, 256)
    padded_2 = pad_oaep(inp, 256)
    print('Padded 1:', padded_1)
    print('Padded 2:', padded_2)
    if padded_1 == padded_2:
        raise AssertionError("Both padding runs produced the same string, which should not be true.")

    unpadded_1 = unpad_oaep(padded_1)
    unpadded_2 = unpad_oaep(padded_2)
    print("Decoded 1:", unpadded_1)
    print("Decoded 2:", unpadded_2)
    if unpadded_1 != unpadded_2:
        raise AssertionError("Decoded message produced different strings.")

    print("SUCCESS: Randomness")
    print_separator()

def test_oaep_shape():
    print_separator()
    print('Running EME-OAEP five times with message "Konpeko"')
    inp = "Konpeko".encode("utf-8")
    res = [pad_oaep(inp, 256) for _ in range(5)]
    for i, padded in enumerate(res):
        print(f"Padded {i + 1}:", padded)

    len_1 = len(res[0])
    if any(len(p) != len_1 for p in res):
        raise AssertionError("Produced padded messages of different lengths.")

    print(f"Produced uniform-length padded messages of length {len_1} bytes")
    print("SUCCESS: Shape")
    print_separator()

def test_oaep_var_length_correctness():
    print_separator()
    print('Running EME-OAEP with output lengths: 128, 256, 384, and 512 bytes')
    inp = b'HELLO!'
    print(f'Input: {inp}')
    lengths = [128, 256, 384, 512]

    res = [pad_oaep(inp, l) for l in lengths]

    for i, out in enumerate(res):
        if (len(out) != lengths[i]):
            raise AssertionError(f"OAEP returned unpadded message of wrong length {len(out)} for {lengths[i]}-byte padding.")
        
        unpadded = unpad_oaep(out)
        if (unpadded != inp):
            raise AssertionError(f"Incorrectly unpadded input bytes {inp} to {unpadded}")
        
        print(f"{lengths[i]} bytes: {unpadded}")

    print("SUCCESS: Correctness at variable lengths")
    print_separator()
    

def test_oaep():
    print("STARTING TESTS FOR OAEP")
    test_oaep_correctness()
    test_oaep_randomness()
    test_oaep_shape()
    test_oaep_var_length_correctness()

    print("OAEP: Passed all tests")
    print_separator()

test_oaep()


from lib.primes import get_mr_rounds
from lib.primes import test_mr

def test_primes_nist_table():
    print_separator()
    rsa_2048_1 = (1024, 2**-100, 4)
    rsa_2048_2 = (1024, 2**-112, 5)
    rsa_3072_1 = (1536, 2**-100, 3)
    rsa_3072_2 = (1536, 2**-128, 4)
    rsa_4096_1 = (2048, 2**-100, 2)
    rsa_4096_2 = (2048, 2**-144, 4)

    checks = [rsa_2048_1, rsa_2048_2, rsa_3072_1, rsa_3072_2, rsa_4096_1, rsa_4096_2]
    print("Testing against NIST standards:")
    for c in checks:
        print(f"RSA{c[0]*2} - {str(c[1])} error probability")

    print()
    for c in checks:
        calced = get_mr_rounds(c[0], c[1])
        print(f"Calculated rounds needed for RSA{c[0]*2}: {calced}")
        print(f"NIST table says: {c[2]} rounds")
        print()
        if (calced != c[2]):
            raise AssertionError(f"Rounds calculator returned {calced}, NIST table says {c[2]}")

    print("SUCCESS: NIST table sanity check")
    print_separator()

def test_primes_even():
    print_separator()
    print("Testing primality of numbers 2^1024 to 2^1124...")
    for i in range(101):
        n = 2**(1024 + i)
        res = test_mr(n, 2**-100)
        if (res): raise AssertionError(f"Power of 2 {n}^{i} marked prime by MR test.")

    print("SUCCESS: 2^1024 to 2^1124 all marked as composite")
    print_separator()

def test_primes_mersenne():
    print_separator()
    print("Testing Mersenne primes 15 to 25 [2^1279-1, 2^21701-1]...")
    nums = [2**1279-1, 2**2203-1, 2**2281-1, 2**3217-1, 2**4253-1, 2**9689-1, 2**9941-1, 2**11213-1, 2**19937-1, 2**21701-1]
    for i, num in enumerate(nums):
        res = test_mr(num, 2**-100)
        if (not res): raise AssertionError(f"Mersenne number #{15 + i} (idx {i}) marked as composite by MR test.")
    print("SUCCESS: Mersenne primes 15 to 25 all marked as prime by MR test ")
    print_separator()

def test_primes():
    test_primes_nist_table()
    test_primes_even()
    test_primes_mersenne()
    print("Primes: Passed all tests")
    print_separator()

# test_primes()

from lib.rsa import RSA

def test_rsa_correctness():
    print_separator()
    print("Testing RSAES correctness with modulus lengths 1024, 2048, 3072, 4096")
    inp = "これは日本語の文です This is an English sentence".encode('utf-8')
    print(f"Input: {inp}")

    lengths = [1024, 2048, 3072, 4096]
    rsaes = [RSA().key_len(l).initialize_rsa() for l in lengths]
    encrypted = [r.rsaes_encrypt(inp) for r in rsaes]
    decrypted = [r.rsaes_decrypt(encrypted[i]) for i, r in enumerate(rsaes)]

    for i, d in enumerate(decrypted):
        if (d != inp):
            raise AssertionError(f"Incorrect RSA decryption detected in RSA {lengths[i]}")

        print(f"Decrypted text matches plaintext for RSA {lengths[i]}")

    print("Success: Correctness across different RSA moduli lengths")
    print_separator()

def test_rsa_randomness():
    print_separator()
    print("Testing RSAES randomness with modulus lengths 1024 and 2048 across 10 encryptions")
    inp = b"HELLLOOOOOOOO!!!"
    print(f"Input: {inp}")

    lengths = [1024, 2048]
    for l in lengths:
        rsa = RSA().key_len(l).initialize_rsa()
        encrypted = []
        for _ in range(10):
            encrypted.append(rsa.rsaes_encrypt(inp))

        if (len(encrypted) != len(set(encrypted))):
            raise AssertionError(f"Duplicates found in ciphertext resulting from RSA {l} encryption")

        print(f"Encryption of same plaintext 10x results in unique ciphertext for RSA {l}")

    print("Success: RSAES Randomness")
    print_separator()

def test_rsa():
    test_rsa_correctness()
    test_rsa_randomness()
    print("RSA: Passed all tests")
    print_separator()

test_rsa()