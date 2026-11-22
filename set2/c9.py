def PKCS7(data, block_size):
    """Pads plaintext to fit desire block size using PKCS#7"""
    length = len(data)
    pad_amt = block_size - length % block_size

    for i in range(pad_amt):
        data = data + bytes([pad_amt])

    return data 

if __name__ == "__main__":
    print(PKCS7("YELLOW SUBMARINE".encode(), 20))