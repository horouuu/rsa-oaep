# Benchmarks
## 1. Prime pair generation speed
The following is a table of how fast generating 1000 pairs with 16 CPU cores took (in seconds):

| RSA | 1000 pairs (16 cores) | 1 pair (1 core) |
|-----|-------------------:|-----------------:|
| 512 | 30.29 | 0.55|
| 768 | 49.2 | 0.89 |
| 1024 | 85.38 | 0.83 |
| 2048 | 294.26 | 2.24 |
| 3072 | 576.16 | 4.63 |
| 4096 | 976.66 | 9.03 |
| 8192 | - | 72.96 |

The table was generated using the `misc/gen_primes.py` function with the following commands:
> `py -m misc.gen_primes 1000 512 768 1024 2048 3072 4096`
> `py -m misc.gen_primes 1 512 768 1024 2048 3072 4096 8192`

The 1-core statistics are an average of 10 executions.

Note that while the script expects up to 16 available cores, an execution with 1 iteration only uses one core.

## 2. Cross-tests for primality
1000 key pairs for RSA 512, 768, 1024, 2048, 3072, and 4096 were generated each and cross-checked with the `.isPrime()` function from SymPy, which implements the Baillie-PSW primality test.

-

## 3. Decryption with CRT vs. basic modulo exponentiation
The modulus lengths 1024, 2048, and 4096 were chosen to test the time saved from switching to CRT decryption. The results were as follows:
| RSA | Modulo Exp. | CRT |
| --- | --- | --- |
| 1024 | 2.48s | 0.88s |
| 2048 | 17.72s | 5.23s |
| 4096 | 128.97s | 37.38s | 

Each row here presents approximately a 3x (300%) time-save from switching to CRT.
Use the following command to repeat this experiment:
> `py -m misc.decryption`

## 4. Public key (encryption) operations
The modulus lengths 1024, 2048, and 4096 were chosen to test the time taken to encrypt 1000 plain text messages:
| RSA | Time |
| --- | --- |
| 1024 | 0.05s |
| 2048 | 0.14s |
| 4096 | 0.48s |

The above shows that the encryption time is virtually nothing compared to the decryption time.
Use the following command to repeat this experiment:
> `py -m misc.encryption`

## 5. Wiener's attack
In his [1990 paper](https://www.jannaud.fr/static/download/Travail/wiener.pdf), Wiener presented an attack involving continued fraction expansion on small choices of the decryption integer $d$. He shows that the approximation of the ratio $\frac{e}{n} \approx \frac{k}{dg}$ can be used in the algorithm to find the private exponent $d$. He states that as long as the inequality $kdg < \frac{pq}{\frac{3}{2}(p+q)}$ is met, the algorithm is guaranteed to succeed. Here, $k$ and $g$ are integer terms that are derived from the RSA congruency $ed \equiv 1 \pmod {LCM(p-1, q-1)}$.

Boneh simplified this theorem in his [1999 paper](https://courses.csail.mit.edu/6.857/2014/files/L14-Boneh-TwentyYearsOfAttacksOnTheRSACryptosystem.pdf) and presented the simpler inequality $d<\frac{1}{3}N^{\frac{1}{4}}$ as an upper bound to the size of the private exponent for this theorem to succeed, which was eventually improved to $d<N^{0.292}$.

Considering the above, we may first review RSA's definition of $e$ and $d$, along with the choice of $e$ in this implementation. RSA defines the public and private exponents $e$ and $d$ as integers that satisfy the congruency $ed\equiv1\pmod{\varphi(n)+1}$. From this, we can derive the equation $ed = k\cdot\varphi(n)+1$ for some integer $k$. Assuming $k > 1$, we now have the inequality $ed \geq \varphi(n)+1$, which we can rearrange into $d \geq \frac{\varphi(n)+1}{e}$, as $e > 0$.

Continuing from the above, we may substitute $\varphi(n)=(p-1)(q-1)$, for coprime integers $p\neq q$. In RSA, $p$ and $q$ are always prime numbers, so this equation is always satisfied. We now have $d \geq \frac{(p-1)(q-1)+1}{e} = \frac{n + (p-q) + 2}{2^{16} + 1}$.

Now, let's review the specifications of RFC 8017 that were followed for this implementation:
> - Private prime factor $p$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq p \leq 2^{\frac{nlen}{2}}-1$
> - Private prime factor $q$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq q \leq 2^{\frac{nlen}{2}}-1$

It can be proven from the above that in this implementation, $p < q < \frac{4}{3}p$ is approximately true (assuming the $-\frac{1}{1.5\cdot2^{\frac{nlen}{2}-1}}$ term is insignificant). This means that the bigger number between the prime pair may only be at most $\frac{4}{3}$ times bigger than the other. Seeing as the pair is of similar magnitude, we may approximate $p=q=n^{\frac{1}{2}}$. Substituting this into the above inequality for $d$, we get: $d\geq\frac{n + 2}{2^{16} + 1}$.

From RFC 8017, we know that the lower bound for $(p, q)$ is $\sqrt{2}\cdot2^{\frac{nlen}{2}-1}$, which has been implemented as setting the two most-significant bits in each number to 1 here, resulting in $1.5\cdot2^{\frac{nlen}{2}-1}$. Therefore, $n\gt(1.5\cdot2^{\frac{nlen}{2}-1})^2=(3\cdot2^{\frac{nlen}{2}-2})^2=(9\cdot2^{nlen-4})$.

Substituting the above into the derived minimum inequality for $d$, we get $d\gt\frac{9\cdot2^{nlen-4} + 2}{2^{16} + 1} \approx 9\cdot2^{nlen-20}$. Substituting the minimum value of $n$ into Wiener's inequality for $d$, we get $d \lt \frac{1}{3}(9\cdot2^{nlen-4})^{\frac{1}{4}}=3\cdot2^{\frac{nlen}{4}-1}$. This means that for RSA modulus length $nlen > 27$, $d \geq 3\cdot2^{\frac{nlen}{4}-1}$, which means that Wiener's attack is never guaranteed to succeed against this implementation. 

Even at the conjectured upper bound of $N^{0.5}$ stated in Boneh's work, this implementation guarantees that $d$ always exceeds the upper bound at modulus lengths of 40 and above.

Note that the statement is **never guaranteed**, and not **guaranteed to never** succeed. However, Boneh states that Wiener's attack against RSA is ineffective for large $d$, so it is highly unlikely to succeed for values of $d$ that exceed the upper bound given.

## 6. Manger's attack
-

## 7. PEM serialization and compatibility with OpenSSL
The library includes a functionality to serialize generated keys into `.pem` files using ASN.1 DER encoding. The uploaded examples `/keys/test-private.pem` and `/keys/test-public.pem` can be used with and verified using OpenSSL.

It has been checked that plaintext encrypted using this library can be decrypted by OpenSSL and vice versa, given the encryption specifications match. The following command can be used to produce ciphertext on OpenSSL that will be compatible with this library.
```
openssl pkeyutl -encrypt \
  -pubin \
  -inkey public.pem \
  -in message.txt \
  -out encrypted.bin \
  -pkeyopt rsa_padding_mode:oaep \
  -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256
```

