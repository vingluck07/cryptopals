import os
from Crypto.Cipher import AES
from s2functions import PKCS7, CBC_encrypt, CBC_decrypt, strip_PKCS7

KEY = os.urandom(16)
IV = os.urandom(16)

def encrypt_data(data):
    """takes data and quotes out ; and =, then prepends/appends with the given strings, then encrypts with CBC"""
    prepend = b"comment1=cooking%20MCs;userdata="
    append = b";comment2=%20like%20a%20pound%20of%20bacon"

    new_data = ""
    for i in data:
        if i == ";":
            new_data += "%3B"
        elif i == '=':
            new_data += "%3D"
        else:
            new_data += i

    new_data = PKCS7(prepend + new_data.encode() + append, 16)

    return CBC_encrypt(new_data, KEY, IV)

def admin_checker(ciphertext):
    """Decrypts and unpads using CBC, then checks if ;admin=true; exists in the plaintext"""
    plaintext = strip_PKCS7(CBC_decrypt(ciphertext, KEY, IV))

    if b";admin=true;" in plaintext:
        return True

    return False

def CBC_attacker():
    """Uses CBC bitflipping attacks to inject ;admin=true;"""
    data = ("A" * 16) + "?admin?true?" + ("A" * 4)
    ciphertext = encrypt_data(data)

    ct_array = bytearray(ciphertext)

    ct_array[32] ^= ord("?") ^ ord(";")
    ct_array[38] ^= ord("?") ^ ord("=")
    ct_array[43] ^= ord("?") ^ ord(";")

    return admin_checker(ct_array)

if __name__ == "__main__":
    print(CBC_attacker())