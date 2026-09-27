def xor_one_byte(hexstr, key):
    """takes a hex string and XORs it against one key, returns the XOR in bytes"""
    bytestr = bytes.fromhex(hexstr)

    XORbytes = bytearray()
    for i in range(len(bytestr)):
        XORbytes.append(bytestr[i] ^ key)

    return XORbytes

def score_bytes(bytestr):
    """returns a score for how likely the str is english plaintext"""
    score = 0
    for byte in bytestr:
        if byte > 127:
            # not plaintext
            score -= 1
        elif byte < 32:
            # not plaintext
            score -= 1
        elif byte == 32 or 65 <= byte <= 90 or 97 <= byte <= 122:
            # english alphabet letters (and space)
            score += 1
    return score

def find_key(hexstr):
    """finds a key that returns the highest score"""
    candidates = dict()

    for i in range(256):
        msg = xor_one_byte(hexstr, i)
        score = score_bytes(msg)
        candidates[i] = score

    max_score = 0
    best_key = 0
    for key in candidates:
        if candidates[key] > max_score:
            best_key = key
            max_score = candidates[key]
    return best_key

if __name__ == "__main__":
    ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    key = find_key(ciphertext)
    print(chr(key))
    print(xor_one_byte(ciphertext, key).decode())

