# Implementation of RSA-OAEP
WARNING: Do not use this library to encrypt any sensitive information. It is mostly a prototype library that has not undergone rigorous testing. It should **NOT** be used in production.

**!!! READ !!!** \
All `.pem` keys used in this library will have to be placed in the `/keys` folder found in the project root directory. \
As such, when running any commands, providing the **key name** is sufficient, but any plaintext/cipher text files require a path. \
This is to ensure that all encryption is **COMMITTAL** and that you do not accidentally use your production keys with this library. \
The `/keys` folder come with pre-generated keys, and any further keys generated will be placed there.

Every command that takes `[pkcs_type]` expects either "pkcs1" or "pkcs8". \
OpenSSL keys that are generated **without** the `--traditional` flag will be in PKCS #8 format. \
This library generates **ONLY PKCS #1 keys**. 

## Content
[Module CLI commands](#module-cli-commands)
[Benchmarks](./misc/benchmarks.md)
[Resources/Infodump](./info.md)

## Module CLI Commands
Some functionalities have been packaged as CLI commands for those not looking to interact with the source code. \
All commands here take the `-v` `--verbose` flag for logging. This will print a LOT of things to your terminal if you enable key generation.

### Encryption with PEM key
Produces a binary of the encrypted plaintext file using a supplied key.
`python3 -m encrypt -t [pkcs_type] [public_key_file_name] [plaintext_path]`
Note that the **path** is needed for the plaintext file. \
The resulting binary file will be placed in the same folder as the plaintext file.

### Decryption with PEM key
Decrypts a binary file.
`python3 -m decrypt -t [pkcs_type] [private_key_file_name] [binary_path]`
Note that the **path** is needed for the plaintext file. \
The resulting decrypted file will be placed in the same folder as the binary/ciphertext file.

### Encryption with key generation
Generates keys, encrypts the file, and exports the keys.
`python3 -m gen-encrypt [plaintext_path]`
Note that the keys generated from here will be put in `/keys`. \
It is not recommended to change this behavior.

Flags:
- `k` - Specifies key name. Defaults to current date.

### Key generation
Generates and exports a pair of keys. \
This command will default to RSA-2048 keys.
`python3 -m gen-keys`
Note that the keys generated from here will be put in `/keys`. \
It is not recommended to change this behavior.

Flags
- `-n` Changes the modulus size.
- `-k` Specifies key name. Defaults to current date.