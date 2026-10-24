from lib.rsa import RSA
import time


def benchmark_encryption(modulus_len):
    inp = b'hello :)'
    
    rsa = RSA().key_len(modulus_len).initialize_rsa()

    iter = 100000

    t = time.perf_counter()
    for _ in range(iter):
        rsa.rsaes_encrypt(inp)

    t = time.perf_counter() - t
    print(f"Took {t} seconds to encrypt {iter} times using CRT in RSA {modulus_len}")

if __name__ == '__main__':
    benchmark_encryption(1024)
    benchmark_encryption(2048)
    benchmark_encryption(4096)