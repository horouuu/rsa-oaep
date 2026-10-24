from lib.rsa import RSA

if __name__ == '__main__':
    rsa = RSA(True)
    msg = bytes("HELLO!", 'utf-8')
    rsa.initialize_rsa()


    # encryption / decryption
    ciphertext = rsa.rsaes_encrypt(msg)
    print(ciphertext)

    decrypted = rsa.rsaes_decrypt(ciphertext)
    print(decrypted)

    print(decrypted == msg)