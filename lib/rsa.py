import secrets
import math
import time
import lib.oaep as oaep
from lib.primes import test_mr
from lib.primes import test_composite_small_primes


class RSA:
    def __init__(self, verbose=False, key_len=2048, e=2**16 + 1):
        self.verbose = verbose
        self.key_len = key_len
        self.e = e

        self._d = -1
        self._n = -1
        self._totient = -1

        self._initialized = False

    def _print_log(self, msg: str, newline: bool=False):
        if (self.verbose):
            print(msg, end="\n" + "\n"*newline)

    def _gen_bits(self, bits):
        r = secrets.randbits(bits) | 0b11 << (bits-2) | 0b1
        return r

    def _get_prime(self, bits):
        att = 0
        while True:
            att += 1
            candidate: int = self._gen_bits(bits)
            if ((candidate-1) % self.e == 0):
                self._print_log(f"(candidate - 1) failed co-primality with public exponent e={self.e}")
                continue

            if (test_composite_small_primes(candidate)):
                self._print_log("Candidate is found to be divisible by a small prime < 542, continuing..")
                continue

            if (test_mr(candidate, 2**-100)):
                self._print_log(f"Probable prime found in {att} attempts.", 1)
                return candidate

            self._print_log("Candidate failed Miller-Rabin test, continuing..")

    def _get_candidate_pair(self):    
        k = self.key_len
        c1_len = math.floor(k/2)
        c2_len = math.ceil(k/2)
        lens = [c1_len, c2_len]

        self._print_log("Generating prime pairs p and q...")
        t = time.perf_counter()
        primes = list(map(self._get_prime, lens))
        while (primes[0] == primes[1]):
            self._print_log("Somehow managed to generate p == q! Re-generating...")
            primes = primes = list(map(self._get_prime, lens))

        t = time.perf_counter() - t
        self._print_log(f"Took {round(t, 2)}s to generate prime pairs p and q.")
        return primes


    def _check_parameters(self):
        if (any(x == -1 for x in [self._n, self._totient, self._d])):
            raise ValueError("Improper setup of RSA parameters.")
        self._print_log("All RSA parameters set up and ready to go.")

    def initialize_rsa(self):
        if (self._initialized):
            self._print_log("Object has already been initialized. Skipping initialization..")
            return self
        
        pair = self._get_candidate_pair()
        n = math.prod(pair)
        self._n = n
        self._totient = n - (sum(pair)) + 1
        self._d = pow(self.e, -1, self._totient)

        self._check_parameters()

        self._initialized = True
        return self

    def rsaes_encrypt(self, msg: bytes):
        if (not self._initialized):
            raise RuntimeError("Must initialize RSA class using initialize_rsa() before attempting encryption.")
        # M ^ e mod n for encryption
        # pad with oaep first
        padded = oaep.pad_oaep(msg)
        int_padded = int.from_bytes(padded, byteorder="big")
        encrypted = pow(int_padded, self.e, self._n)
        return encrypted.to_bytes(self.key_len // 8, byteorder="big")

    def rsaes_decrypt(self, cipher: bytes):
        if (not self._initialized):
            raise RuntimeError("Must initialize RSA class using initialize_rsa() before attempting decryption.")
        # C ^ d mod n for decryption
        int_cipher = int.from_bytes(cipher, byteorder="big")
        decrypted = pow(int_cipher, self._d, self._n)
        decrpyted_bytes = decrypted.to_bytes(self.key_len // 8, byteorder="big")

        # now unpad with oaep
        return oaep.unpad_oaep(decrpyted_bytes)