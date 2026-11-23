# Learning Cryptography Through Cryptopals

## Reflection
- AI was very useful in this process because the cryptopals descriptions were sometimes too complex for me to understand and the AI was able to break it down.
- Using AI meant that I didn't have to worry so much about syntax because i could ask it for relevant functions so the focus was fully on understanding how the different cryptographic methods work rather than feeling frustrated by the code.
- The cryptopals challenges are broken down very well so each challenge feels very feasible and is not daunting to tackle

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
    - `.decrypt(ciphertext)`: Used on the cipher object, returns plaintext in bytes
- Takeaways: basic decryption is easy with pycryptodome

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

## Set 2
### Challenge 9
**Goal:** Write a function that pads a byte string to a given block length
- AES only works on full 16 byte blocks so the number of missing bytes gets padded. If the plaintext is exactly 16 bytes, add a full block of padding.
- Padding has to be reversible, so each byte of padding will have a value equal to the number of bytes padded. A depadding function can just read the last byte and know how much padding to remove
- Useful Python tools:
    - `bytes([n])`: a single byte with the value n. (`bytes(n)` would be incorrect and gives n zero bytes)
    - `bytes * int`: repeats a byte string
    - `+`: to concatenate bytes

## Challenge 10
**Goal:** Build CBC mode on top of single block ECB and decrypt the given file using the key "YELLOW SUBMARINE" and an IV of all zero bytes without using the library's CBC mode
- Encrypting with CBC: XOR each plaintext block with the previous ciphertext block and AES encrypt the result. For the first plaintext block, use the IV (Initialization Vector)
- Decrypting with CBC: AES decrypt every block then XOR it with the previous blocks ciphertext (or the IV for the first block)
- EBC had patterns because identical blocks ecrypted identically. This will help reduce the pattern.
- Useful Python tools:
    - `AES.new(key, AES.MODE_ECB)`: Creates a new cipher object
    - `.decrypt(ciphertext)` and `.encrypt(plaintext)`: use on the cipher object to decrypt and encrypt the text
    - `bytes(n)`: returns n zero bytes (used for the IV)
    - `base64.b64decode()`: turns the file data from base 64 to raw ciphertext

## Challenge 11
**Goal:** Build an oracle and a detector. The oracle will take plaintext and append 5-10 random bytes before and after the plaintext (different count for each side), then encrypt it under a random 16-byte key and will randomly choose ECB or CBC (CBC IV will be random). The detector will call the oracle then decide whether ECB or CBC was used.
- The detector should also record what mode it chose to confirm correctess of the detector. (the detector should not have access to the chosen mode)
- Real data is rarely just the plaintext itself due to headers, cookies, tokens and other fillers. The added bytes before and after the plaintext is supposed to mimic that.
- The detector gets to decide what plaintext gets to be sent to the oracle so it makes sense to choose something where any repetition would be extremely obvious (I used `b'A' * 48`).
- If there are ANY repeat bytes at all the detector will know its ECB, otherwise it is CBC. This is because the chance of a repeat in CBC is extremely low (1 / 2^128)
- Useful Python Tools:
    - `random.randint(2)`: Use this for deciding ECB or CBC
    - `os.urandom(16)`: Generates 16 random bytes. Asks the operating system for the 16 bytes which is much more secure than using the random module.
    - `os.urandom(random.randint(5,10))`: Randomly chooses 5-10 bytes for appending and randomly chooses what those bytes will be

## Challenge 12
**Goal:** Overall goal is to break ECB encryption by creating an oracle function and sending repeated calls to the oracle.
- The oracle will append the given string, pad it, and encrypt it. The key will be generated randomly but will be reused once it is generated.
- The attacker will be able to choose the start of the plaintext so it will be like this: `AES-128-ECB(your string || unknown-string, random-key)`
- The cost of this feels very high because you need to build a unique lookup for every single byte of the secret message but it still runs pretty quickly since its a computer. runtime for lookup building is `256 * n` where n is the number of bytes in the secret message. 
- Summarized steps for breaking ECB:
    1. Find block size: add 1 to the input length until ciphertext length jumps, then you will know the block size
    2. Confirm that it is ECB: Use challenge 11 detector to confirm its ECB
    3. Build a lookup: For all 256 byte values, encrypt 15 fillers + that byte to figure out what the first byte is.
    4. Recover the first byte: send block_size - 1 filler bytes so the output has the first byte of the secret.
    5. Repeat: use 14 fillers + the byte you know and so on to break the rest of the message.
    6. Stop when matching fails: this means you reached the padding
- You can condense the coding algorithm to a pretty small chunk of code but there is a lot of room for error in that chunk. Work on it piece by piece and keep building/changing the code to accomodate for longer messages. Start with just the first byte, then a full block, then the entire message.
- Useful Python tools:
    - `for i in range(256): bytes([i])`: generate the candidates of byte values
- Takeaways: this challenge is very dense and takes a lot of problem solving but it feels incredibly real in terms of breaking cryptography. We are using a legit AES encryption method and breaking it which is super cool!