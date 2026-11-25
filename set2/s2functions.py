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

def CBC_decrypt(ciphertext, key, IV):
    """Decrypts using CBC mode on top of single block ECB, returns plaintext in bytes"""
    ciphertext_blocks = []
    for i in range(0, len(ciphertext), 16):
        ciphertext_blocks.append(ciphertext[i:i+16])

    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = b''
    prev = IV
    for i in ciphertext_blocks:
        decrypted = cipher.decrypt(i)
        plaintext += bytes_XOR(decrypted, prev)
        prev = i

    return plaintext

def validate_PKCS7(data):
    """Takes padded data and checks if it is PKCS#7"""
    n = data[-1]
    padding = data[-n:]

    if n > 16:
        return False

    i = 0
    for byte in padding:
        if byte != n:
            return False
        i += 1

    if i != n:
        return False
    else:
        return True

def strip_PKCS7(data):
    """Checks that data is padded with PKCS#7 and strips the padding"""
    if not validate_PKCS7(data):
        raise ValueError("padding is not valid PKCS#7")

    n = data[-1]
    return data[:-n]