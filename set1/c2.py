def hex_XOR(str1, str2):
    """Takes 2 hex strings and XORs them to produce 1 hex string"""
    bytes1 = bytes.fromhex(str1)
    bytes2 = bytes.fromhex(str2)

    XORbytes = bytearray()
    for i in range(0, len(bytes1)):
        XORbytes.append(bytes1[i] ^ bytes2[i])

    return XORbytes.hex()

if __name__ == "__main__":
    str1 = "1c0111001f010100061a024b53535009181c"
    str2 = "686974207468652062756c6c277320657965"
    if hex_XOR(str1, str2) == "746865206b696420646f6e277420706c6179": print("Correct Output")
    else: print("ERROR: Incorrect Output")