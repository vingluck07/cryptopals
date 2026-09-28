from c3 import xor_one_byte, score_bytes, find_key


def find_XOR_encrypt(filename):
    """Finds the line that is most likely to be 1-byte XOR encryption. returns key and decrypted plaintext"""
    keyscores = dict()
    
    with open(filename) as f:
        for line in f:
            line = line.strip()
            keyscores[line] = find_key(line)

    key = 0
    bestline = ""
    score = 0
    for line in keyscores:
        if keyscores[line][1] > score:
            key = keyscores[line][0]
            bestline = line
            score = keyscores[line][1]

    return chr(key), xor_one_byte(bestline, key).decode().strip()


if __name__ == "__main__":
    filename = "c4-data.txt"
    print(find_XOR_encrypt(filename))