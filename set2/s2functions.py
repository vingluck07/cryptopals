from Crypto.Cipher import AES

def PKCS7(data, block_size):
    """Pads plaintext to fit desire block size using PKCS#7"""
    length = len(data)
    pad_amt = block_size - length % block_size

    for i in range(pad_amt):
        data = data + bytes([pad_amt])

    return data 

def bytes_XOR(str1, str2):
    """Takes 2 byte strings and XORs them to produce 1 byte string"""
    XORbytes = bytearray()
    for i in range(0, len(str1)):
        XORbytes.append(str1[i] ^ str2[i])

    return XORbytes

def CBC_encrypt(plaintext, key, IV):
    """Encrypts using CBC mode on top of single block ECB, returns ciphertext in bytes"""
    plaintext_blocks = []
    for i in range(0, len(plaintext), 16):
        plaintext_blocks.append(plaintext[i:i+16])

    cipher = AES.new(key, AES.MODE_ECB)

    ciphertext = b''
    prev = IV
    for i in plaintext_blocks:
        encrypted = cipher.encrypt(bytes_XOR(i, prev))
        prev = encrypted
        ciphertext += encrypted

    return ciphertext