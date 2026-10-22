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

[RFC 8017](https://www.rfc-editor.org/info/rfc8017/#section-6)
1. (7.1) RSAES-OAEP
2. (7.1.1) Encryption Operation
3. (7.1.2) Decryption Operation
4. (B.2.1) MGF1
    - MGF1 will be implemented as dictated in Appendix B of RFC 8017.

## 1. Implementation Details
The `secrets` library in Python will be used to securely generate random numbers.
In RSA2048, prime candidates $p$ and $q$ are 1024-bit integers.
### 1.1 Pertaining to Generation of Key Pairs (A.1.1) of NIST FIPS 186-5
1. This implementation will use the method of "probable primes" to generate its primes $p$ and $q$.
    - The Miller-Rabin test is used to test the primality of prime candidates.
### 1.2 Pertaining to IFC Key Standards (A.1.1) of NIST FIPS 186-5
1. The public exponent $e$ shall be the value $2^{16} + 1$, or $65537$.
    - This number satisfies the NIST standard range for $e$, namely $2^{16} < e < 2^{256}$.
    - This number has a very low hamming weight of $HW(65537) = 2$.
    - The above property is used in the square-and-multiply algorithm for efficient calculations.
2. The two left-most bits of $p$ and $q$ candidates will be set to 1 to satisfy the 3rd and 4th points of [2] in the pertaining section above.
    - This is done to fit the lower bound of the constraints above. 
    - The left-most bit ensures that the number is at least $2^{\frac{nlen}{2}-1}$, and the 2nd left-most bit ensures that the value $0.5\cdot2^{\frac{nlen}{2}-1}$ is added.
    - Together, they make up $1.5\cdot2^{\frac{nlen}{2}-1} > \sqrt{2}\cdot2^{\frac{nlen}{2}-1}$ 

3. The right-most bit of $p$ and $q$ condidates will be set to 1 to ensure that the number is odd.
### 1.3 Pertaining to RFC 8017
1. The chosen hash function is SHA256.
2. The value for `lHash` will be hard coded as `(0x)e3b0c442 98fc1c14 9afbf4c8 996fb924 27ae41e4 649b934c a495991b 7852b855` (SHA256).
    - This is done to simplify the implementation of RSAES-OAEP.
3. The chosen MGF is MGF1.

## 2. Mechanism of Random Prime Generation
The mechanism is roughly as follows:
1. A random number of length `k` is generated using `secrets.randbits`.
2. The first two bits of the number is set to 1, along with the LSB, as detailed in [section 1.2](#pertaining-to-ifc-key-standards-a11-of-nist-fips-186-5).
3. The number is divided by 5 and rejected if the modulo returns 0.
4. The number is divided by the first 100 prime numbers and rejected if the modulo returns 0.
5. The number is passed through the Miller-Rabin test.
6. If accepted, then the number is used as a prime candidate.

## Miscellaneous
List of Mersenne primes taken from [mersenne.org](https://www.mersenne.org/primes/)