def repeat_XOR(plaintext, key):
    """Encrypts the plaintext with the key using repeating-key XOR. Returns encrypted hexstring"""
    plainbytes = plaintext.encode()
    keybytes = key.encode()

    encryptbytes = bytearray()
    i = 0
    for byte in plainbytes:
        encryptbytes.append(byte ^ keybytes[i])
        i = (i + 1) % len(key)

    return encryptbytes.hex()


if __name__ == "__main__":
    plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    if repeat_XOR(plaintext, key) == expected: print("Correct Output")
    else: print("ERROR: Incorrect Output")