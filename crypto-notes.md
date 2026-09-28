# Learning Cryptography Through Cryptopals

## Set 1
### Challenge 1
**Goal:** Write a function that takes the hex string given and produce the matching base64 string. (hex string -> raw bytes -> base64 string)
- It's impoortant to only work on raw bytes since cyphers work on the bytes themselves (ex. XORing two hex strings will produce garbage but XORing the bytes they represent gives the correct answer.)
- Some numbers to remember:
    - 8 bits in a byte
    - Hex: each byte is 2 characters (4 bits per character)
    - Base64: every 3 bytes is 4 characters (6 bits per character)\
- Useful Python tools:
    - `bytes.fromhex(s)`: turns hex string into a bytes object
    - `base64.b64encode(b)`: turns bytes into base64 (returns bytes)
    - `.decode()`: turns result into a string
    - `bytes.hex()`, `base64.b64decode()`: do the opposite of above, useful for checking work

### Challenge 2
**Goal:** Write a function that takes 2 equal length buffers and produces the XOR
- Useful Python tools:
    - `^`: performs the XOR function
    - `bytearray()`: mutable bytes that supports .append(int)
    - `.hex()`: converts bytes into hex

### Challenge 3
**Goal:** Given a hex string that has been XORed with a single character, figure out that character and decrypt the message
- Devise a scoring method for english plaintext to see which one is a real message.
- There are 256 possible values for a single byte
- Useful Python tools:
    - `dict()`: makes an empty dictionary
    - `d[key] = value`: to make new key or update key value
    - `.decode(errors="replace")`: Makes it so an unknown characters get replaced with � instead of breaking
    -`chr(int)`: turns a single byte-int into a character
- Scoring for Plaintext:
    - +1 for alphabet characters and space
    - -1 for byte > 127: anything above 127 isn't commonly used characters
    - -1 for byte < 32: anything below 32 is non plaintext stuff

### Challenge 4
**Goal:** Given a file with 327 encrypted hex strings (60 characters) with exactly 1 encrypted with single-byte XOR, find the string with the single-byte XOR encryption.
- Rough outline:
    - Seperate the file into lines
    - For each line, perform what challenge 3 was designed to do
    - Compare all the lines and extract the one with the highest score
- Useful Python tools:
    - `with open("FILENAME") as f:`: opens the file and closes it when code is done
    - `for line in f:`: iterates over each line
    - `.strip()`: removes the \n from a line
    - `from ... import ...: allows reuse of functions from challenge 3