from Crypto.Cipher import AES
import os
from s2functions import PKCS7

KEY = os.urandom(16)

def kv_parser(data):
    """takes foo=bar&baz=qux&zap=zazzle and parses into a dictionary"""
    items = data.split("&")

    user = dict()
    for pair in items:
        split = pair.split("=")
        user[split[0]] = split[1]

    return user

def profile_for(email):
    """encodes the email into a user profile and returns the encoding"""
    # & and = cannot be allowed in the email
    if ("&" in email) or ("=" in email):
        raise ValueError("email cannot contain & or =")

    return f"email={email}&uid=10&role=user"

def profile_encrypt(profile):
    """takes encoded profile and encrypts it"""
    padded = PKCS7(profile.encode(), 16)
    
    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded)

    return ciphertext

def profile_decrypt(ciphertext):
    """decrypts the profile and parses into a dict"""
    cipher = AES.new(KEY, AES.MODE_ECB)
    data = cipher.decrypt(ciphertext)

    len_pad = data[-1]
    profile = data[:-len_pad]

    return kv_parser(profile.decode())

def profile_attacker():
    """Abuses ECB to manipulate ciphertext for an admin account, returns tampered ciphertext"""
    email = "abc@gmail.com" #must be 13 characters

    ciphertext = profile_encrypt(profile_for(email))
    block1 = ciphertext[:-16]
    block2 = profile_encrypt("admin")

    return block1 + block2


if __name__ == "__main__":
    ciphertext = profile_attacker()
    print(profile_decrypt(ciphertext))