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
1000 key pairs for RSA 512, 768, 1024, 2048, 3072, and 4096 were generated each and cross-checked with the `prime` command from OpenSSL, which implements several tests, including Miller-Rabin.

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

# Analysis on the Effectiveness of Wiener's Attack

In 1990, [Wiener](https://ieeexplore.ieee.org/document/54902/) presented an attack involving continued fraction expansion on small choices of the decryption integer $d$. He shows that the approximation of the ratio $\frac{e}{n} \approx \frac{k}{dg}$ can be used in the algorithm to find the private exponent $d$. He states that as long as the inequality $kdg < \frac{pq}{\frac{3}{2}(p+q)}$ is met, the algorithm is guaranteed to succeed. In his paper, $k$ and $g$ are integer terms that are derived from the RSA congruency $ed \equiv 1 \pmod{\lambda(n)}$. Note that this version uses the Carmichael function instead of Euler's totient function.

Boneh simplifies this theorem in his [1999 paper](https://www.semanticscholar.org/paper/e85c8789db8a9379c60a1621878222bcbe7a11a3) and presents the simpler inequality $d < \frac{1}{3}N^{\frac{1}{4}}$ as an upper bound to the size of the private exponent for this theorem to succeed, which [Boneh and Durfee](https://link.springer.com/chapter/10.1007/3-540-48910-X_1) eventually raised to $d < N^{0.292}$ using a different attack to Wiener, where $N$ is the RSA modulus. Note that in this project, we refer to the modulus as the lowercase $n$. To investigate the strength of the choice of our parameters, we will use Boneh and Durfee's threshold as a conservative threshold.

Considering the above, we may first review RSA's definition of $e$ and $d$, along with the choice of $e$ in this implementation. Our implementation defines the public and private exponents $e$ and $d$ as integers that satisfy the congruency $ed \equiv 1 \pmod{\varphi(n)}$. From this, we can derive the equation $ed = k\cdot\varphi(n)+1$ for some integer $k$. Assuming $k \geq 1$, we now have the inequality $ed \geq \varphi(n)+1$, which we can rearrange into $d \geq \frac{\varphi(n)+1}{e}$, as $e > 0$.

Continuing from the above, we may substitute $\varphi(n)=(p-1)(q-1)$, for distinct primes $p\neq q$. We now have:

$$
d \geq \frac{(p-1)(q-1)+1}{e}
$$

Now, let us review the specifications of NIST FIPS-186-5 [nist2023fips1865] that were followed for this implementation:

- Private prime factor $p$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq p \leq 2^{\frac{nlen}{2}}-1$
- Private prime factor $q$ must be selected randomly and must satisfy $\sqrt{2}\cdot 2^{\frac{nlen}{2}-1} \leq q \leq 2^{\frac{nlen}{2}}-1$

Our implementation in particular sets the two left-most bits to 1 (along with the right-most bit to ensure oddness), which means that every prime is within the following bound:

$$
1.5\cdot2^{\frac{nlen}{2}-1} \leq p \leq 2^{\frac{nlen}{2}}-1
$$

Now, we may rearrange the totient, taking the minimum value for both $p$ and $q$:

$$
\begin{aligned}
\varphi(n) &\geq (1.5\cdot2^{\frac{nlen}{2}-1}-1)(1.5\cdot2^{\frac{nlen}{2}-1}-1)\\
\varphi(n) &\geq (1.5\cdot2^{\frac{nlen}{2}-1}-1)^2
\end{aligned}
$$

We now have a lower bound for the value of $d$ in this implementation:

$$
\begin{aligned}
d &\geq \frac{\varphi(n)+1}{e}\\
d &\geq \frac{(1.5\cdot2^{\frac{nlen}{2}-1}-1)^2+1}{65537}
\end{aligned}
$$

The upper bound for the modulus $n$ in our implementation is the same as the NIST FIPS-186-5 specification [nist2023fips1865], that is:

$$
n \leq (2^{\frac{nlen}{2}}-1)^2
$$

Substituting this into Boneh's threshold of $n^{0.292}$ gives us:

$$
\begin{aligned}
T &= n^{0.292} \leq ((2^{\frac{nlen}{2}}-1)^2)^{0.292}\\
T &\leq (2^{\frac{nlen}{2}}-1)^{0.584}\\
T &< (2^{\frac{nlen}{2}})^{0.584} = 2^{0.292\cdot nlen}
\end{aligned}
$$

As $2^{\frac{nlen}{2}}>2^{\frac{nlen}{2}}-1$.

Now, to simplify the lower bound for $d$:

$$
\begin{aligned}
\text{Let } x &= 2^{\frac{nlen}{2}-1}\\
\therefore\quad d &\geq \frac{(1.5x-1)^2+1}{65537}
\end{aligned}
$$

We can simplify the inner term of the lower bound by turning it into a more conservative minimum. Note that in our implementation, $x$ is guaranteed to be at least 2:

$$
\begin{aligned}
\text{For } x &\geq 2,\quad 1.5x-1\geq x\\
\therefore\quad (1.5x-1)^2 &\geq x^2\\
\therefore\quad d &\geq \frac{(2^{\frac{nlen}{2}-1})^2}{65537}
=\frac{2^{nlen-2}}{65537}
\end{aligned}
$$

Now, we set $d$ to be at least at the threshold, finding for the minimum value for $nlen$:

$$
\begin{aligned}
d &\geq T\\
\frac{2^{nlen-2}}{65537} &\geq 2^{0.292\cdot nlen}\\
2^{nlen-2} &\geq 65537\cdot2^{0.292\cdot nlen}\\
nlen-2 &\geq \log_2(65537)+0.292\cdot nlen\\
0.708nlen &\geq \log_2(65537)+2\\
nlen &\geq \frac{\log_2(65537)+2}{0.708}\\
nlen &\geq 26\quad\text{(rounded up)}
\end{aligned}
$$

We can see that with our implementation and parameters, 26 bits is a sufficient modulus size for the private exponent to be above Boneh's threshold, which means that it also exceeds the bound for the threshold prescribed for Wiener's attack. While this does not guarantee that the attacks are **incapable** of succeeding, it does mean that the conditions for Wiener's (and Boneh's) attacks are not satisfied within our system.

## 6. Manger's attack
https://www.iacr.org/archive/crypto2001/21390229.pdf
Not implemented. Research purposes only.

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

