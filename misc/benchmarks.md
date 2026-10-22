# Benchmarks
## 1. Prime pair generation speed
The following is a table of how fast generating 1000 pairs with 16 CPU cores took (in seconds):

| RSA | Seconds (16 cores) | Seconds (1 core) |
|-----|--------------------|------------------|
| 512 | 30.29 |
| 768 | 49.2 |
| 1024 | 85.38 |
| 2048 | 294.26 |
| 3072 | 576.16 |
| 4096 | - |

The table was generated using the `misc/gen_primes.py` function with the following commands:
> `py -m misc.gen_primes 1000 512 768 1024 2048 3072 4096`
> `py -m misc.gen_primes 1 512 768 1024 2048 3072 4096`
Note that while the script expects up to 16 available cores, an execution with 1 iteration only uses one core.