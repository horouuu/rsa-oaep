import sys
import argparse
from lib.rsa import RSA
from pathlib import Path
from lib.prints import print_log

parser = argparse.ArgumentParser()

parser.add_argument("key")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-n", type=int, default=2048)

if __name__ == '__main__':
    args = parser.parse_args()
    key_path = Path(Path(__file__).resolve().parent / "keys" / args.key)

    if (args.n < 1024):
        print_log("This library does not support modulus lengths under 1024.", True)
        sys.exit(1)

    rsa = RSA().verbose(args.verbose).key_len(args.n)
    rsa.initialize_rsa()
    rsa.serialize_pkcs_1(str(key_path))