import secrets
import math
import time
from lib.primes import test_mr
from lib.primes import test_composite_small_primes

verbose = False
key_len = 2048

class RSA:
    def __init__(self, verbose=False, key_len=2048):
        self.verbose = verbose
        self.key_len = key_len

    def print_log(self, msg: str, newline: bool=False):
        if (self.verbose):
            print(msg, end="\n" + "\n"*newline)

    def gen_bits(self, bits):
        r = secrets.randbits(bits) | 0b11 << (bits-2) | 0b1
        return r

    def get_prime(self, bits):
        att = 0
        while True:
            att += 1
            candidate: int = self.gen_bits(bits)
            if (test_composite_small_primes(candidate)):
                self.print_log("Candidate is found to be divisible by a small prime < 100, continuing..")
                continue

            if (test_mr(candidate, 2**-100)):
                self.print_log(f"Probable prime found in {att} attempts.", 1)
                return candidate

            self.print_log("Candidate failed Miller-Rabin test, continuing..")

    def get_candidate_pair(self):    
        k = self.key_len
        c1_len = math.floor(k/2)
        c2_len = math.ceil(k/2)
        lens = [c1_len, c2_len]

        self.print_log("Generating prime pairs p and q...")
        t = time.perf_counter()
        primes = list(map(self.get_prime, lens))
        t = time.perf_counter() - t
        self.print_log(f"Took {round(t, 2)}s to generate prime pairs p and q.")
        return primes

    # TODO: CHECK IF P = Q