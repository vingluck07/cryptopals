import base64


def hex_to_base64(hexstr):
    """converts a hex string to a base64"""
    hexbytes = bytes.fromhex(hexstr)
    b64bytes = base64.b64encode(hexbytes)
    return b64bytes.decode()


if __name__ == "__main__":
    hexstr = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    if hex_to_base64(hexstr) == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t": print("Correct Output")
    else: print("ERROR: Incorrect Output")