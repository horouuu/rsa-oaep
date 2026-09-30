# Implementation of RSA-OAEP in RSA2048

## Resources
[Appendix A of NIST FIPS 186-5](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf)
1. (A.1.1) Criteria for IFC Key Pairs (Generation of Key Pairs)
    - Both $p$ and $q$ must both be prime numbers and be one of the following:
        - Provable primes
        - Probable primes
2. (A.1.1) Criteria for IFC Key Pairs (IFC Key Standards) 
    - Public exponent $e$ must be an **odd positive integer** such that $2^{16} < e < 2^{256}$
    - $(p - 1)$ and $(q - 1)$ must be relatively prime to the public exponent $e$
    - Private prime factor $p$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq p \leq 2^{\frac{nlen}{2}}-1$
    - Private prime factor $q$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq q \leq 2^{\frac{nlen}{2}}-1$
    - $|p-q| > 2^{\frac{nlen}{2}-100}$
3. (A.1.3) Generation of Random Primes That Are Probably Prime

## Implementation Details
### Pertaining to Generation of Key Pairs (A.1.1) of NIST FIPS 186-5
1. This implementation will use the method of "probable primes" to generate its primes $p$ and $q$.
### Pertaining to IFC Key Standards (A.1.1) of NIST FIPS 186-5
1. The public exponent $e$ shall be the value $2^{16} + 1$, or $65537$.
    - This number satisfies the NIST standard range for $e$, namely $2^{16} < e < 2^{256}$.
    - This number has a very low hamming weight of $HW(65537) = 2$.
    - The above property is used in the square-and-multiply algorithm for efficient calculations.
