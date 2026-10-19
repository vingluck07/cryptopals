import base64
from c3 import find_key

MAX_KEYSIZE = 40

def hamming_dist(str1, str2):
    """finds the hamming distance between two byte strings"""
    diff_bits = 0
    for i in range(0, len(str1)):
        diff_bits += (str1[i] ^ str2[i]).bit_count()

    return diff_bits


def find_keysize(cipher):
    """find the most likely KEYSIZE for ciphertext"""
    min_dist = float("inf")
    best_keysize = 0

    for keysize in range(2, MAX_KEYSIZE + 1):
        str_list = []
        dist_list = []
        for i in range(len(cipher) // keysize):
            str_list.append(cipher[i*keysize:(i+1)*keysize])

        for i in range(len(str_list) - 1):
            dist_list.append(hamming_dist(str_list[i], str_list[i+1]))

        norm_avg = (sum(dist_list) / len(dist_list)) / keysize

        if norm_avg < min_dist:
            min_dist = norm_avg
            best_keysize = keysize

    return best_keysize

def decrypt_block_XOR(cipher, key):
    """takes a ciphertext and returns the plaintext decrypted with the key
    
    Args:
        cipher: ciphertext in bytes
        key: key as str
    Returns:
        decrypted plaintext as str    
    """
    key = key.encode()

    decryptbytes = bytearray()
    i = 0
    for byte in cipher:
        decryptbytes.append(byte ^ key[i])
        i = (i + 1) % len(key)
    
    return decryptbytes.decode()

def decrypt_XOR(cipher):
    """finds the most likely key and decrypts the cipher with it

    Args: 
        cipher: ciphertext in bytes
    Returns: 
        (plaintext, key) tuple, both as str
    """
    #input: ciphertext, output: tuple(plaintext, key)
    keysize = find_keysize(cipher)

    block_list = []
    for i in range(keysize):
        block_list.append(cipher[i::keysize])

    key = str()
    plaintext = str()
    for i in block_list:
        key = key + chr(find_key(i.hex())[0])

    return decrypt_block_XOR(cipher, key), key

if __name__ == "__main__":
    with open("c6-data.txt") as f:
        cipher = base64.b64decode(f.read())

    decrypted = decrypt_XOR(cipher)
    print(f"{decrypted[0]}\n{decrypted[1]}")