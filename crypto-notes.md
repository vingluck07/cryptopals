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

### Challenge 5
**Goal:** Encrypt a long message with a repeating key XOR.
- In repeating-key XOR, each byte of the key will be sequentially applied to each byte of the plaintext (aka Vigenere cipher in XOR form)
- it is weaker because the repeating key... repeats
- Useful Python tools:
    - `.encode()`: turns plaintext into bytes
    - `.hex()`: turns result into a hexstring

### Challenge 6
**Goal:** Take a file that has been encrypted with repeating key XOR and decrypt it
1. let KEYSIZE be the guessed length of the key (2-40)
2. Write a function to compute the Hamming Distance (# of differing bits) between two strings
3. For each KEYSIZE, find hamming distance between the first and second KEYSIZE worth of bytes and divide by KEYSIZE to normalize (or take more blocks and average the distances for more accuracy)
    - `cipher[n*keysize:(n+1)*keysize]` will give the n-th byte block.
4. The KEYSIZE with the smallest hamming distance is probably the keysize
5. Break the ciphertext into blocks of KEYSIZE length
6. Transpose the blocks: make a block that is the first byte of every block, block that is the second byte of every block, ect...
7. Solve each block as if it was single-char XOR
8. For each block, the single byte XOR key with the highest score is the XOR key for that block.
- Useful Pythol tools:
    - `base64.b64decode()`: turns base64 into bytes (use to decode the whole file before proceeding)
    - `(a ^ b).bit_count()`: returns the number of differing bits. `.bit_count()` returns the number of bits that are 1, when a and b are XORed, differing bits will output as 1.
    - `zip(a, b)`: pairs up bytes of a and b 
    - `data[i::k]`: returns every kth element starting at i (useful for transposing step)
- Takeaways: using hamming distance is an interesting way to compare different key lengths. It works because each byte will have similarities if it is encrypted with the same letter. you can try different key lengths and figure out what length makes the bytes most similar. Then we can apply methods we already used before to find the key and decrypt.

### Challenge 7
**Goal:** Take a base64 file that is encrypted with AES-128 in ECB mode and decrypt with the given key.
- AES only encrypts one 16 byte block, the mode defines how to handle longer messages
- ECB mode encrypts each block independently with the same key (it's not secure due to repetition)
- Useful Python tools:
    - crypto library is required. pycryptodome is a good option
    - `AES.new(key, AES.MODE_ECB)`: creates a cipher object (usually named cipher)
    - `.decode(ciphertext)`: Used on the cipher object, returns plaintext in bytes
- Takeaways: basic decryption is ez with pycryptodome

### Challenge 8
**Goal:** In a file full of hex-encoded ciphertexts, figure out which one is encrypted with ECB.
- ECB is deterministic, the same 16-byte block always produces the same 16-byte ciphertext
- Real data has a lot of unintentional repetition such as formatting with padding and headers.
- Split the lines and strip them like challenge 4
- Split each ciphertext into 16-byte blocks and count how many are duplicates
- Useful Python tools:
    - `bytes.fromhex()`: to get bytes from the hex
    - `set()`: removes duplicates, subtract from original to get # of duplicates
- Takeaways: Repetition makes ECB easy to detect but it still is hard to crack since its encrypted with AES. Without the key, there are far too many possibilities to realistically be able to brute force. This challenge just shows how you can see where plaintext is repeated in ECB