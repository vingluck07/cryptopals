import os
import base64
from s2functions import PKCS7
from Crypto.Cipher import AES

KEY = os.urandom(16)
SECRET = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
BLOCK_SIZE = 16

def ECB_oracle(plaintext):
    """Encrypts under ECB global variables, SECRET and KEY"""
    data = plaintext + SECRET

    pad_data = PKCS7(data, BLOCK_SIZE)

    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad_data)

    return ciphertext

def find_block_size():
    """finds the block size that the oracle uses, returns block_size and len_secret"""
    text = b"A"
    len1 = len(ECB_oracle(text))
    len2 = 0
    while len1 >= len2:
        text = text + b"A"
        len2 = len(ECB_oracle(text))

    block_size = len2 - len1
    len_secret = len1 - len(text)

    return block_size, len_secret

def is_ECB(block_size):
    """checks if the oracle uses ECB"""
    plaintext = b'A' * 48

    ciphertext = ECB_oracle(plaintext)
    
    ciphertext_blocks = []
    for i in range(0, len(ciphertext), block_size):
        ciphertext_blocks.append(ciphertext[i:i+block_size])

    ciphertext_set = set(ciphertext_blocks)
    if len(ciphertext_set) < len(ciphertext_blocks):
        return True
    else:
        return False

def ECB_attacker():
    """Breaks ECB by taking advantage of adding known plaintext to the start of the secret"""
    # Find block size
    block_size, len_secret = find_block_size()

    # Checks if oracle uses ECB
    if not is_ECB(block_size):
        return "ORACLE DOES NOT USE ECB, CANNOT CONTINUE"

    lookup = dict()
    known = b""

    for j in range(len_secret):
        b = 16 * (j // 16) # Starting index of the current block

        # Fill in the lookup dict
        filler = b"A" * (15 - (len(known) % 16))
        for i in range(256):
            lookup[i] = ECB_oracle(filler + known + bytes([i]))[b : b + 16]

        # Recover one byte and add it to known
        ciphertext = ECB_oracle(filler)[b : b + 16]

        for key in lookup:
            if ciphertext == lookup[key]:
                known += bytes([key])
                break

        lookup.clear()
    
    return known

if __name__ == "__main__":
    print("*** OBTAINED OUTPUT ***")
    print(ECB_attacker().decode())
    print("*** EXPECTED OUTPUT ***")
    print(SECRET.decode())
