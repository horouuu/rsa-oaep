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

def test_oaep():
    print("STARTING TESTS FOR OAEP")
    test_oaep_correctness()
    test_oaep_randomness()

test_oaep()