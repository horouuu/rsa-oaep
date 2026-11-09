from lib.oaep import pad_oaep
from lib.oaep import unpad_oaep
from uuid import uuid4
from pathlib import Path

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

def test_oaep_rejection():
    print_separator()
    print("Testing OAEP rejections")
    msg = b"HELLO"
    print(f"Encoding message: {msg} with OAEP..")
    enc = pad_oaep(msg, 256)
    print(f"Testing for rejection vector 1: initial zero-byte")
    nozero = bytes(0x11) + enc[1:]

    try:
        unpad_oaep(nozero)
        raise AssertionError("OAEP did not reject an encoded value with missing/corrupted zero-bytes.")
    except ValueError:
        print("OAEP successfully rejected message with missing/corrupted zero-bytes.")

    print("Now testing corruption of every bit...")
    for i in range(2048):
        corrupted = (int.from_bytes(enc) ^ (1 << i)).to_bytes(len(enc), "big")
        try:
            unpad_oaep(corrupted)
            raise AssertionError("OAEP did not reject an encoded value with missing/corrupted bits.")
        except ValueError:
            pass
    print("OAEP successfully rejected corruption of every single bit.")
    print("SUCCESS: OAEP Rejection")
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
    test_oaep_rejection()
    test_oaep_randomness()
    test_oaep_shape()
    test_oaep_var_length_correctness()

    print("OAEP: Passed all tests")
    print_separator()

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

def cleanup_test_keys(keys: list[Path]):
    for key in keys:
        key = Path(__file__).resolve().parent / ".." / "keys" / key
        Path(str(key) + "-public.pem").unlink()
        Path(str(key) + "-private.pem").unlink()
        print(f"[CLEANUP] Deleted key pair {key}")

def test_key_correctness():
    print_separator()
    print("Testing two PKCS #1-serialized RSA-1024 keys for correctness...")
    msg = b"HELLO THERE!"
    print(f"Message: {msg}")

    rsa1_name = str(uuid4())
    rsa2_name = str(uuid4())
    keys = [rsa1_name, rsa2_name]

    try:
        rsa1 = RSA().key_len(1024).initialize_rsa()
        rsa1.serialize_pkcs_1(str(rsa1_name))

        rsa2 = RSA().key_len(1024).initialize_rsa()
        rsa2.serialize_pkcs_1(str(rsa2_name))

        rsa1_test = RSA().key_len(1024).import_key("pkcs1", str(rsa1_name) + "-private.pem")
        rsa2_test = RSA().key_len(1024).import_key("pkcs1", str(rsa2_name) + "-private.pem")

        print("Successfully serialized and re-imported both keys.")

        rsa1_cipher = rsa1.rsaes_encrypt(msg)
        rsa2_cipher = rsa2.rsaes_encrypt(msg)

        rsa1_decrypt = rsa1_test.rsaes_decrypt(rsa1_cipher)
        rsa2_decrypt = rsa2_test.rsaes_decrypt(rsa2_cipher)

        if (rsa1_decrypt != msg):
            cleanup_test_keys(keys)
            raise AssertionError("First RSA-1024 key failed to decrypt ciphertext correctly.")

        if (rsa2_decrypt != msg):
            cleanup_test_keys(keys)
            raise AssertionError("Second RSA-1024 key failed to decrypt ciphertext correctly.")

        print(f"Success! Both RSA-1024 keys resolved the message: {msg}")
        print(f"PKCS #1 import/export also validated")
    finally:
        cleanup_test_keys(keys)
        print_separator()

def test_pkcs8_import():
    print_separator()
    print("Testing import and compatibility of pre-generated OpenSSL PKCS #8 key...")
    priv = Path(".test") / "test-pkcs8-ssl-private.pem"
    pub = Path(".test") / "test-pkcs8-ssl-public.pem"
    keys = [str(k) for k in [priv, pub]]

    msg = b"HEEEEEELLLLLOOOOOOO!!"

    print(f"Attempting encryption and decryption with message: {msg}")

    rsa = RSA().import_key("pkcs8", keys[0], keys[1])
    c = rsa.rsaes_encrypt(msg)
    d = rsa.rsaes_decrypt(c)

    if (d != msg):
        raise AssertionError(f"PKCS #8 key {keys[pub]}/{keys[priv]} failed to encrypt/decrypt message {msg}")
    else:
        print(f"Successfully encrypted/decrypted message {msg}")

    print_separator()

def test_pem():
    test_key_correctness()
    test_pkcs8_import()
    print("PEM: Passed all tests")
    print_separator()

test_oaep()
test_primes()
test_rsa()
test_pem()
print("Done:")
print("OAEP - PASSED")
print("Primes - PASSED")
print("RSA - PASSED")
print("PEM - PASSED")
