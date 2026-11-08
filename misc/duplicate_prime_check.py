import ast
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "out"
rsa = [512, 768, 1024, 2048, 3072, 4096]
for r in rsa:
    with open(OUT_DIR / f"primes-[RSA{r}]-1k.txt", "r") as f:
        arr = ast.literal_eval(f.read())
        size = len(arr)
        set_size = len(set(arr))

        if (size != set_size):
            print(f"Found {size - set_size} duplicate prime occurrences in RSA{r} file.")
        else:
            print(f"RSA{r} file passed duplicate prime test.")

        print(f"Prime count: {size}")