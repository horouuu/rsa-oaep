from lib.rsa import RSA

if __name__ == '__main__':
    # Example using imported PKCS #1 key generated from this library.
    # Alternatively, you can generate the keys instead by commenting the `rsa.import_key("pkcs1", "_ssl-private.pem", "_ssl-public.pem")` line.
    # This may take extra processing power and thus time, depending on your device.

    # Note:
    # You may need to change the key length on a weaker device.
    # I would not recommend using RSA 8192 or higher on weaker devices.
    ###

    rsa = RSA().verbose(True).key_len(2048)

    rsa.import_key("pkcs1", "test-private.pem", "test-public.pem")
    rsa.initialize_rsa()

    m = bytes("HELLO!", 'utf-8')
    c = rsa.rsaes_encrypt(m)
    d = rsa.rsaes_decrypt(c)

    # print(c) # <--- This will definitely pollute your terminal, but you can uncomment it if interested.
    print(d)

    ###
    # Feel free to try out the rest of the library.
    # In general, functions without an underscore (_) are meant for public use.
    # You should only ever need the following:
    #
    # rsa.initialize_rsa()
    # rsa.rsaes_encrypt(msg_bytes)
    # rsa.rsaes_decrypt(ciphertext_bytes)
    # rsa.import_key(pkcs_type, pk_filename, sk_filename (optional))
    # rsa.verbose(bool)
    # rsa.key_len(len)
    #
    # But, you're free to use the internal functions as needed, too.