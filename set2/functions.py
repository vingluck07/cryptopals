def bytes_XOR(str1, str2):
    """Takes 2 byte strings and XORs them to produce 1 byte string"""
    XORbytes = bytearray()
    for i in range(0, len(str1)):
        XORbytes.append(str1[i] ^ str2[i])

    return XORbytes