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
    min_dist = MAX_KEYSIZE
    best_keysize = 0

    for keysize in range (2, MAX_KEYSIZE + 1):
        str1 = cipher[0:keysize]
        str2 = cipher[keysize:2*keysize]
        str3 = cipher[2*keysize:3*keysize]
        str4 = cipher[3*keysize:4*keysize]

        dist1 = hamming_dist(str1, str2)
        dist2 = hamming_dist(str2, str3)
        dist3 = hamming_dist(str3, str4)
        dist4 = hamming_dist(str1, str4)

        norm_avg = ((dist1 + dist2 + dist3 + dist4) / 4) / keysize

        if norm_avg < min_dist:
            min_dist = norm_avg
            best_keysize = keysize

    return best_keysize

def decrypt_XOR(cipher):
    """finds and returns the decrypted plaintext and the key"""
    keysize = find_keysize(cipher)

    block_list = []
    for i in range(keysize):
        block_list.append(cipher[i:keysize])

    key = str()
    for i in block_list:
        key = key + str(find_key(i.hex())[0])

    print(key.decode())

if __name__ == "__main__":
    with open("c6-data.txt") as f:
        cipher = base64.b64decode(f.read())

    print(decrypt_XOR(cipher))