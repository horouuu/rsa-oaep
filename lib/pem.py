import base64
from pathlib import Path
import textwrap
from typing import Literal


def get_tag(tag_class: int, constructed: int, tag_number: int):
    if not (0 <= tag_class <= 3):
        raise ValueError("Invalid tag class")
    if constructed not in (0, 1):
        raise ValueError("Invalid constructed flag")
    if not (0 <= tag_number < 31):
        raise ValueError("Tag numbers >30 not implemented")

    tag = (tag_class << 6) | (constructed << 5) | tag_number
    return bytes([tag])

def construct_tlv(tag: bytes, value: bytes):
    v_len = len(value)
    if (v_len < 128):
        len_bytes = bytes([v_len])
    else:
        extra = (v_len.bit_length() + 7) // 8
        len_bytes = bytes([0x80 | extra]) + v_len.to_bytes(extra, "big")
    return tag + len_bytes + value

def int_to_bytes(n: int):
    length = max(1, (n.bit_length() + 7) // 8)
    res = n.to_bytes(length, "big")
    if (res[0] & 0x80):
        res = b"\x00" + res

    return res

def sequence(tlvs: list[bytes]):
    seq_tag = get_tag(0, 1, 16) # sequence tag
    return construct_tlv(seq_tag, b"".join(tlvs))

def integer(i: int):
    int_bytes = int_to_bytes(i)
    tag = get_tag(0, 0, 2) # integer tag
    return construct_tlv(tag, int_bytes)

def export_pkcs1(filename: str, seq_bytes: bytes, key_type: Literal["private", "public"]):
    OUT_DIR = Path(__file__).resolve().parent.parent / "keys"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    encoded = base64.b64encode(seq_bytes).decode("ascii")

    pem = (
    f"-----BEGIN RSA {key_type.upper()} KEY-----\n"
    + "\n".join(textwrap.wrap(encoded, 64))
    + f"\n-----END RSA {key_type.upper()} KEY-----\n"
    )

    filename = filename.split('.')[0]

    with open(OUT_DIR / f"{filename}-{key_type}.pem", "w") as f:
        f.write(pem)