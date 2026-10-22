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
> `py -m misc.avg_primes 1 512 768 1024 2048 3072 4096 8192`

The 1-core statistics are an average of 10 executions.

Note that while the script expects up to 16 available cores, an execution with 1 iteration only uses one core.