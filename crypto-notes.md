# Learning Cryptography Through Cryptopals

## Set 1
### Challenge 1
**Goal:** Take the hex string given and produce the matching base64 string. (hex string -> raw bytes -> base64 string)
- It's impoortant to only work on raw bytes since cyphers work on the bytes themselves (ex. XORing two hex strings will produce garbage but XORing the bytes they represent gives the correct answer.)
- Some numbers to remember:
    - 8 bits in a byte
    - Hex: each byte is 2 characters (4 bits per character)
    - Base64: every 3 bytes is 4 characters (6 bits per character)\
- Useful Python tools:
    - bytes.fromhex(s): turns hex string into a bytes object
    - base64.b64encode(b): turns bytes into base64 (returns bytes)
    - .decode(): turns result into a string
    - bytes.hex(), base64.b64decode(): do the opposite of above, useful for checking work