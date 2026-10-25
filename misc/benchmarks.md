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
-

## 6. PEM serialization and compatibility with OpenSSL
-