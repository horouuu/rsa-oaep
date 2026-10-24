from lib.rsa import RSA
import time


def benchmark_decryption(modulus_len):
    inp = b'hello :)'
    
    rsa = RSA().key_len(modulus_len).initialize_rsa()
    cipher = rsa.rsaes_encrypt(inp)

    iter = 1000

    t = time.perf_counter()
    for _ in range(iter):
        rsa.rsaes_decrypt(cipher)

    t = time.perf_counter() - t
    print(f"Took {t} seconds to decrypt {iter} times using CRT in RSA {modulus_len}")

    t = time.perf_counter()
    for i in range(iter):
        rsa._decrypt_basic(cipher)

    t = time.perf_counter() - t
    print(f"Took {t} seconds to decrypt {iter} times using modulo exponentiation in RSA {modulus_len}")

if __name__ == '__main__':
    benchmark_decryption(1024)
    benchmark_decryption(2048)
    benchmark_decryption(4096)