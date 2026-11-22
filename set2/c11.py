import os
import random
from Crypto.Cipher import AES
from s2functions import PKCS7, CBC_encrypt

def generate_AES_key():
    """returns a random AES key (16 bytes)"""
    return os.urandom(16)

def ECB_CBC_oracle(plaintext):
    """adds 5-10 random bytes before and after plaintext, then randomly encrypts with ECB or CBC and returns the ciphertext"""
    before = os.urandom(random.randint(5,10))
    after = os.urandom(random.randint(5,10))

    padded_text = PKCS7(before + plaintext + after, 16)

    mode = random.randrange(2)
    if mode == 0: #ECB mode
        print("oracle chose ECB mode")
        cipher = AES.new(generate_AES_key(), AES.MODE_ECB)
        ciphertext = cipher.encrypt(padded_text)
    elif mode == 1: #CBC mode
        print("oracle chose CBC mode")
        ciphertext = CBC_encrypt(padded_text, generate_AES_key(), os.urandom(16))

    return ciphertext

def ECB_CBC_detector():
    """calls the oracle and guesses if the ciphertext is ECB or CBC"""
    plaintext = b'A' * 48

    ciphertext = ECB_CBC_oracle(plaintext)
    
    ciphertext_blocks = []
    for i in range(0, len(ciphertext), 16):
        ciphertext_blocks.append(ciphertext[i:i+16])

    ciphertext_set = set(ciphertext_blocks)
    if len(ciphertext_set) < len(ciphertext_blocks):
        print("detector guesses ECB")
    else:
        print("detector guesses CBC")

    return


if __name__ == "__main__":
    ECB_CBC_detector()