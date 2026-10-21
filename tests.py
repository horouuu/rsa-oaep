from oaep import pad_oaep
from oaep import unpad_oaep

def print_separator():
    print("------------------------------------------")

def test_oaep_correctness():
    print_separator()
    print('Running EME-OAEP with message "HELLO"')
    inp = bytes("HELLO", 'utf-8')
    padded = pad_oaep(inp)
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
    padded_1 = pad_oaep(inp)
    padded_2 = pad_oaep(inp)
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
    res = [pad_oaep(inp) for _ in range(5)]
    for i, padded in enumerate(res):
        print(f"Padded {i + 1}:", padded)

    len_1 = len(res[0])
    if any(len(p) != len_1 for p in res):
        raise AssertionError("Produced padded messages of different lengths.")

    print(f"Produced uniform-length padded messages of length {len_1} bytes")
    print("SUCCESS: Shape")
    print_separator()

def test_oaep():
    print("STARTING TESTS FOR OAEP")
    test_oaep_correctness()
    test_oaep_randomness()
    test_oaep_shape()

    print("OAEP: Passed all tests")
    print_separator()

test_oaep()


from primes import get_mr_rounds

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

    print("SUCCESS: NIST Table Sanity Check")
    print_separator()

def test_primes():
    test_primes_nist_table()
    print("Primes: Passed all tests")
    print_separator()

test_primes()