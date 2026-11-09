def print_log(msg: str, err: bool=False):
    prefix = "[*] "
    if (err):
        prefix ="[ERROR] "

    print(prefix + msg)