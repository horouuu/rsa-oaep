import hashlib
import math
import secrets

# implementation of mgf1
def _mask(maskLen: int, seed: bytes):
    hash_len = 32
    if (maskLen > 2**32 * hash_len):
        raise ValueError("Specified mask length too long.")

    M = bytearray()
    for i in range(0, math.ceil(maskLen/hash_len)):
        c = i.to_bytes(4, byteorder="big")
        hash_inp = seed + c
        hash = hashlib.sha256(hash_inp).digest()
        M.extend(hash)

    return bytes(M[:maskLen])

# helper function for bitwise XOR
def _xor_bytes(a, b):
    if len(a) != len(b):
        raise ValueError("Length of byte strings a and b must be the same.")

    return bytes(x ^ y for x, y in zip(a, b))

def pad_oaep(message: bytes, out_len: bytes):
    msg_len = len(message)
    hash_len = 32
    if (msg_len > out_len - hash_len*2 - 2):
        raise ValueError("Message length too long.")
    
    label_hash = hashlib.sha256(bytes('', 'utf-8')).digest()
    ps = (0).to_bytes(out_len - msg_len - 2*hash_len - 2, byteorder="big")
    db = label_hash + ps + b"\x01" + message

    seed = secrets.token_bytes(hash_len)
    masked_db = _xor_bytes(db, _mask(out_len - hash_len - 1, seed))
    masked_seed = _xor_bytes(seed, _mask(hash_len, masked_db))
    return b"\x00" + masked_seed + masked_db

def unpad_oaep(padded_msg: bytes):
    label_hash = hashlib.sha256(b"").digest()
    msg_len = len(padded_msg)
    hash_len = 32
    masked_seed = padded_msg[1:hash_len+1]
    masked_db = padded_msg[hash_len+1:msg_len]

    seed_mask = _mask(hash_len, masked_db)
    seed = _xor_bytes(masked_seed, seed_mask)
    db_mask = _mask(msg_len - hash_len - 1, seed)
    db = _xor_bytes(db_mask, masked_db)

    recovered_label = db[0:hash_len]
    msg_idx = db.find(b"\x01", hash_len)

    if msg_idx == -1:
        raise ValueError("Decryption error: no separator")

    if any(b != 0 for b in db[hash_len:msg_idx]):
        raise ValueError("Decryption error: non-zero value in PS")

    if (recovered_label != label_hash):
        raise ValueError("Received different label hashes")

    return db[msg_idx+1:]
