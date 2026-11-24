def validate_PKCS7(data):
    """Takes padded data and checks if it is PKCS#7"""
    n = data[-1]
    padding = data[-n:]

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

if __name__ == "__main__":
    print(strip_PKCS7(b"ICE ICE BABY\x04\x04\x04\x04"))
    print(validate_PKCS7(b"ICE ICE BABY\x05\x05\x05\x05"))
    print(validate_PKCS7(b"ICE ICE BABY\x01\x02\x03\x04"))