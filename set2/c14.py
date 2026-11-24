import random
import os
import base64
from Crypto.Cipher import AES
from s2functions import PKCS7

PREFIX = os.urandom(random.randint(1, 64))
KEY = os.urandom(16)
SECRET = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
BLOCK_SIZE = 16


def ECB_oracle(plaintext):
    """Encrypts under ECB global variables, SECRET and KEY. Prepends a prefix and appends the secret"""
    data = PREFIX + plaintext + SECRET

    pad_data = PKCS7(data, BLOCK_SIZE)

    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad_data)

    return ciphertext

def find_prefix_len():
    """finds the length of the prefix and returns it"""
    filler = b"A" * 32
    for i in range(16):
        ciphertext = ECB_oracle(filler)

        prev = ciphertext[0:16]
        for j in range(16, len(ciphertext), 16):
            if ciphertext[j:j+16] == prev:
                return j - i - 16
            prev = ciphertext[j:j+16]
        filler += b"A"

    return -1 #something went wrong

def find_len_secret():
    """finds the length of the secret and returns it"""
    text = b"A"
    len1 = len(ECB_oracle(text))
    len2 = 0
    while len1 >= len2:
        text = text + b"A"
        len2 = len(ECB_oracle(text))

    len_secret = len1 - len(text)

    return len_secret

def ECB_attacker():
    """Breaks ECB by taking advantage of adding known plaintext to the start of the secret"""
    # Find length of the prefix
    len_prefix = find_prefix_len()
    prefix_buffer = b"A" * (16 - (len_prefix % 16))
    len_chunk1 = len_prefix + len(prefix_buffer) #first chunk to ignore when solving

    # Find length of the secret
    len_secret = find_len_secret() - len_prefix

    # Adjust original code to account for extra buffer for prefix
    lookup = dict()
    known = b""

    for j in range(len_chunk1, len_secret + len_chunk1):
        b = 16 * (j // 16) # Starting index of the current block

        # Fill in the lookup dict
        filler = b"A" * (15 - (len(known) % 16)) + prefix_buffer
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
    print(ECB_attacker().decode())