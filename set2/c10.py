import base64
from Crypto.Cipher import AES
from functions import bytes_XOR

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


if __name__ == "__main__":
    with open("c10-data.txt") as f:
        ciphertext = base64.b64decode(f.read())

    key = "YELLOW SUBMARINE".encode()
    IV = bytes(16)

    decrypted = CBC_decrypt(ciphertext, key, IV)
    encrypted = CBC_encrypt(decrypted, key, IV)
    print(decrypted.decode())
    if encrypted == ciphertext:
        print("Encryption works as well")
    else:
        print("Encryption incorrect")    