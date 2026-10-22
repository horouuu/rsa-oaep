import math
import secrets
def test_composite_small_primes(num: int):
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337,347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
    return any(num % p == 0 for p in small_primes)

# Based on NIST FIPS 186-5 Appendix C.1
# The equation for p_(k,t) here has been simplified. Details in README.md.
def calc_p3(m: int, t: int, bits: int):
    outer = 0
    for j in range(3, m+1):
        inner = 0
        for k in range(2, j+1):
            inner += 2**-(k + (bits-1)/k)
        outer += 2**(j - (j-1)*t) * inner

    return outer

def get_mr_rounds(bits: int, target: float):
    upper_t = math.ceil(-math.log2(target)/2) 
    upper_m = math.floor(2*(math.sqrt(bits-1)) - 1)
    for t in range(1, upper_t+1):
        for m in range(3, upper_m+1):
            p_1 = 2.00743 * math.log(2) * bits
            p_2 = 8/3 * (math.pi**2 - 6)
            p_3 = calc_p3(m, t, bits)
            p = p_1*(2**(-2-m*t)) + p_1*p_2*(2**-2)*p_3
            if (p <= target):
                return t

    return -1

def test_mr(w: int, target_err: float):
    # w-1 here is always even, as w is always odd
    a = 0
    m = (w - 1) 

    while (m % 2 == 0):
        a += 1
        m //= 2

    wlen = w.bit_length()
    rounds = get_mr_rounds(wlen, target_err)
    if (rounds < 1):
        raise ValueError("MR rounds returned value lower than 1. Perhaps the number given is too small.")
    
    for _ in range(rounds):
        # only works for w >= 4, which is much smaller than RSA standards
        b = secrets.randbelow(w - 3) + 2
        z = pow(b, m, w)

        if (z == 1 or z == w - 1): continue
        else:
            for _ in range(1, a):
                z = pow(z, 2, w)
                if (z == w - 1): break
                elif (z == 1): return False
            else:
                return False

    return True