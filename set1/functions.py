# CONTAINS FUNCTIONS THAT ARE USED BETWEEN CHALLENGES

def xor_one_byte(hexstr, key):
    """takes a hex string and XORs it against one key, returns the XOR in bytes"""
    bytestr = bytes.fromhex(hexstr)

    XORbytes = bytearray()
    for i in range(len(bytestr)):
        XORbytes.append(bytestr[i] ^ key)

    return XORbytes

def find_key(hexstr):
    """finds a key that returns the key and the highest score"""
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
    return best_key, max_score