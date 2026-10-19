def find_AES_ECB(ciphertext_list):
    """Finds the ciphertext that is likely to be AES-128 in ECB mode

    Args:
        ciphertext_list: list containing each ciphertext as bytes
    Returns:
        a single ciphertext that is likely to be ECB in bytes 
    """
    max_repeats = 0
    best_ciphertext = b""
    for ciphertext in ciphertext_list:
        blocks = []
        for i in range(len(ciphertext)//16):
            blocks.append(ciphertext[i*16:i*16+16])

        repeats = len(blocks) - len(set(blocks))
        if repeats > max_repeats:
            max_repeats = repeats
            best_ciphertext = ciphertext

    return best_ciphertext

if __name__ == "__main__":
    lines = []
    with open("c8-data.txt") as f:
        for line in f:
            line = line.strip()
            lines.append(bytes.fromhex(line))

    print(find_AES_ECB(lines))