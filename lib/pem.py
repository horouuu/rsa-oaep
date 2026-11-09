import base64
from pathlib import Path
import textwrap
from typing import Literal

ASN1_TAGS: dict[str, int] = {
    "INTEGER": 0x02,
    "OCTET_STRING": 0x04,
    "NULL": 0x05,
    "OBJECT_IDENTIFIER": 0x06,
    "SEQUENCE": 0x30,
    "BIT_STRING": 0x03
}

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

def import_pkcs(filename: str, encoding: Literal["pkcs1"] | Literal["pkcs8"]) -> list[int]:
    # limit scope to /keys in project root
    OUT_DIR = Path(__file__).resolve().parent.parent / "keys"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / filename, "r") as f:
        pem = f.read()

    base64str = "".join(pem.strip().split("\n")[1:-1])
    decoded = base64.b64decode(base64str)
    if (encoding.lower() == "pkcs1"):
        key_type, content = parse_pkcs1(decoded)
    elif (encoding.lower() == "pkcs8"):
        key_type, content = parse_pkcs8(decoded)
    else:
        raise ValueError(f"Unexpected key encoding {encoding}")
    
    parsed = [int.from_bytes(b, "big") for b in content]

    return key_type, parsed

def parse_pkcs1(seq: bytes):
    content, _ = parse_tlv(seq, ASN1_TAGS["SEQUENCE"])
    rsa_parameters = [] 
    while (content):
        val, content = parse_tlv(content, ASN1_TAGS["INTEGER"])
        rsa_parameters.append(val)

    param_len = len(rsa_parameters)
    if (param_len == 2):
        return ("public", rsa_parameters)

    if (param_len == 9):
        ver = int.from_bytes(rsa_parameters[0])
        if (ver == 0):
            return ("private", rsa_parameters)
        else:
            raise ValueError("RSA private keys with version other than 0 are not supported by this library.")

    raise ValueError("Invalid RSA key imported.")

def parse_tlv(tlv_bytes: bytes, code: int):
    parsed_code = tlv_bytes[0]
    if (parsed_code != code):
        raise ValueError(f"Unexpected code: {parsed_code.to_bytes().hex()} (should be {code.to_bytes().hex()})")

    content_bytes = parse_len(tlv_bytes[1:])
    return content_bytes

def parse_len(len_bytes: bytes):
    len = len_bytes[0]
    len_bytes_n = 0
    if (len > 0x80):
        len_bytes_n = len & 0x7F
        len = len_bytes[1:1+len_bytes_n]
        len = int.from_bytes(len, "big")
    elif (len == 0x80):
        raise ValueError("Illegal indefinite length tag for SEQ tag detected. This is not allowed in DER.")

    start = 1 + len_bytes_n
    seq_bytes = len_bytes[start:start+len]

    return seq_bytes, len_bytes[start+len:]

def parse_pkcs8(seq: bytes):
    content, _ = parse_tlv(seq, ASN1_TAGS["SEQUENCE"])

    # public keys don't have the VERSION TLV here
    if (content[0] == ASN1_TAGS["INTEGER"]):
        version, nxt = parse_tlv(content, ASN1_TAGS["INTEGER"])
        if (int.from_bytes(version) != 0):
            raise ValueError("RSA private keys with versions other than 0 are not supported by this library.")
        alg_cont, nxt = parse_tlv(nxt, ASN1_TAGS["SEQUENCE"])
    else:
        alg_cont, nxt = parse_tlv(content, ASN1_TAGS["SEQUENCE"])

    obj, nxt_alg = parse_tlv(alg_cont, ASN1_TAGS["OBJECT_IDENTIFIER"])
    null, nxt_alg = parse_tlv(nxt_alg, ASN1_TAGS["NULL"])
    
    if (obj.hex() != "2a864886f70d010101"):
        raise ValueError("Algorithm type in imported key is not RSA (1.2.840.113549.1.1.1 / 2a864886f70d010101).")

    if (null):
        raise ValueError("Null parameter contained other, valid bytes.")

    if (nxt[0] == ASN1_TAGS["BIT_STRING"]):
        rsa_content, nxt = parse_tlv(nxt, ASN1_TAGS["BIT_STRING"])
        rsa_content = rsa_content[1:]
    else:
        rsa_content, nxt = parse_tlv(nxt, ASN1_TAGS["OCTET_STRING"])

    print(rsa_content)
    return parse_pkcs1(rsa_content)