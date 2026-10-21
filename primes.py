import math

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
