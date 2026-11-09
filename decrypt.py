import sys
import argparse
from lib.rsa import RSA
from pathlib import Path
from lib.prints import print_log

parser = argparse.ArgumentParser()

parser.add_argument("bin")
parser.add_argument("key")
parser.add_argument("-t", "--type", type=str.lower, choices=["pkcs1", "pkcs8"], required=True)
parser.add_argument("-v", "--verbose", action="store_true")

if __name__ == '__main__':
    args = parser.parse_args()
    key_path = Path(Path(__file__).resolve().parent / "keys" / args.key)
    binary_path = Path(args.bin)

    if (not key_path.exists()):
        print_log(f"Key file {key_path} not found. Make sure it's in the project's /keys folder.", True)
        sys.exit(1)

    if (not binary_path.exists()):
        print_log(f"Binary file at path {binary_path} not found.", True)
        sys.exit(1)

    rsa = RSA().verbose(args.verbose)
    rsa.import_key(args.type, args.key)
    rsa.decrypt_file(args.bin)