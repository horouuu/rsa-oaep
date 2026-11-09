import sys
import argparse
import datetime
from lib.rsa import RSA
from pathlib import Path
from lib.prints import print_log

parser = argparse.ArgumentParser()

parser.add_argument("plain")
parser.add_argument("-k", "--key")
parser.add_argument("-n", type=int, default=2048)
parser.add_argument("-v", "--verbose", action="store_true")

if __name__ == '__main__':
    args = parser.parse_args()
    key_name = args.key
    if (not key_name):
        key_name = datetime.date.today().isoformat()

    plaintext_path = Path(args.plain)

    if (args.n < 1024):
        print_log("This library does not support modulus lengths under 1024.", True)
        sys.exit(1)

    if (not plaintext_path.exists()):
        print_log(f"Plaintext file at path {plaintext_path} not found.", True)
        sys.exit(1)

    rsa = RSA().verbose(args.verbose).key_len(args.n)
    rsa.initialize_rsa()
    rsa.encrypt_file(plaintext_path)
    rsa.serialize_pkcs_1(key_name)