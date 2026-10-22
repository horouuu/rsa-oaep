from lib.rsa import RSA
from multiprocessing import Pool
import sys
from pathlib import Path
import time
# !!! WARNING
# THIS IS A VERY EXPENSIVE PROCESS
# THIS SCRIPT WAS MADE UNDER THE ASSUMPTION THAT THE HOST DEVICE HAS A 16-CORE CPU
# IT MAY TAKE A LONG TIME TO GENERATE 1,000 PAIRS WITH SINGLE-CORE DEVICES


def gen_test_pairs(key_len: int):
    rsa = RSA(False, key_len)
    return rsa.get_candidate_pair()

if __name__ == '__main__':
    if (len(sys.argv) < 2 or int(sys.argv[1]) < 1):
        raise ValueError("Must have at least 1 iteration")
    iterations = sys.argv[1]
    
    if (len(sys.argv) < 3 or int(sys.argv[2]) < 512):
        raise ValueError("Use at least a 512-bit key.")
    key_vars = sys.argv[2:]
    
    print(f"Executing gen_primes with {iterations} iterations and the following variations:")
    for var in key_vars:
        print(f"RSA{var}")


    OUT_DIR = Path(__file__).resolve().parent / "out"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for var in key_vars:
        t = time.perf_counter()
        print(f"Generating {iterations} key pairs for RSA{var}...")
        with Pool(16) as pool:
            primes = pool.map(gen_test_pairs, [int(var)] * iterations)
        primes = [x for sublist in primes for x in sublist]
        t = time.perf_counter() - t
        print(f"Generated {iterations} pairs of RSA{var} keys in {round(t, 2)} seconds.\n")
        with open( OUT_DIR / f"primes-[RSA{var}].txt", "w") as f:
            f.write(str(primes))