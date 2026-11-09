from lib.rsa import RSA

if __name__ == '__main__':
    rsa = RSA().verbose(True).key_len(2048)
    msg = bytes("HELLO!", 'utf-8')

    rsa._import_pkcs1_private_key("_ssl-private.pem")