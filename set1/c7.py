import base64
from Crypto.Cipher import AES

def AES_ECB_decrypt(ciphertext, key):
    """Decrypts the ciphertext with the key using AES-128 in ECM mode
        
    Args:
        ciphertext: ciphertext in bytes
        key: key in bytes
    Returns:
        plaintext as a str
        """
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()

if __name__ == "__main__":
    key = "YELLOW SUBMARINE"
    with open("c7-data.txt") as f:
            cipher = base64.b64decode(f.read())

    print(AES_ECB_decrypt(cipher, key.encode()))