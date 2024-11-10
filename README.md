# RC4 and AES Algorithms

This project implements two cryptographic algorithms: **RC4**, a stream cipher, and **AES (Advanced Encryption Standard)**, a block cipher. Both algorithms are widely used in cryptography for their unique features. This document provides a detailed overview of each algorithm, including implementation details, methodologies, and usage instructions.

---

### Table of Contents
1. [Overview](#overview)
2. [RC4 Algorithm](#rc4-algorithm)
   - [Key Scheduling Algorithm (KSA)](#key-scheduling-algorithm-ksa)
   - [Pseudo-Random Generation Algorithm (PRGA)](#pseudo-random-generation-algorithm-prga)
   - [Encryption/Decryption Function](#encryptiondecryption-function)
3. [AES Algorithm](#aes-algorithm)
   - [Substitution and Permutation Steps](#substitution-and-permutation-steps)
   - [Rounds and Key Expansion](#rounds-and-key-expansion)
4. [Installation and Usage](#installation-and-usage)
5. [Code Examples](#code-examples)

---

## Overview
**RC4** and **AES** are two types of encryption algorithms used to protect data. RC4 is a stream cipher known for its simplicity and efficiency, while AES is a block cipher recognized for its security and widespread adoption in various security protocols. Each algorithm is implemented with its respective key scheduling, encryption, and decryption processes.

---

## RC4 Algorithm

### Methodology
The RC4 algorithm, designed by Ron Rivest in 1987, is a symmetric stream cipher known for its speed and simplicity. It encrypts by generating a pseudorandom keystream, which is XORed with the plaintext to produce the ciphertext. This process is also used in reverse for decryption.

#### 1. Key Scheduling Algorithm (KSA)
The Key Scheduling Algorithm (KSA) initializes a state vector `S`, which is a permutation of 256 possible byte values (0–255). The state vector `S` is then scrambled based on the key to create a key-dependent permutation, which is subsequently used in the Pseudo-Random Generation Algorithm to produce the keystream. 

**Implementation:**
```python
def rc4_key_scheduling(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S
```

#### 2. Pseudo-Random Generation Algorithm (PRGA)
The PRGA generates the keystream by continually modifying the state vector `S`. This keystream is then XORed with the plaintext or ciphertext for encryption or decryption.

**Implementation:**
```python
def rc4_pseudo_random_generation(S, plaintext_length):
    i = j = 0
    keystream = []
    for _ in range(plaintext_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    return keystream
```

#### 3. Encryption/Decryption Function
In RC4, encryption and decryption are symmetric due to the XOR operation, making the same function applicable for both processes.

**Implementation:**
```python
def rc4_encrypt(plaintext, key):
    S = rc4_key_scheduling(key)
    keystream = rc4_pseudo_random_generation(S, len(plaintext))
    ciphertext = bytes([plaintext[i] ^ keystream[i] for i in range(len(plaintext))])
    return ciphertext
```

---

## AES Algorithm

### Methodology
AES (Advanced Encryption Standard) is a symmetric block cipher known for its strong security. It operates on fixed-size blocks (typically 128 bits) and uses rounds of substitution and permutation operations based on a secret key to encrypt data.

#### Substitution and Permutation Steps
AES encryption and decryption are structured as multiple rounds of transformations, including **SubBytes** (substitution), **ShiftRows** (row shifting), **MixColumns** (column mixing), and **AddRoundKey** (key addition). Each round, except the final one, includes all transformations. These transformations introduce diffusion and confusion, essential for robust encryption.

#### Rounds and Key Expansion
AES uses a specified number of rounds (10, 12, or 14) depending on the key size (128, 192, or 256 bits). A key schedule expands the initial key to generate round keys, which are added to the state at each round.

**Key Expansion Implementation:**
```python
def aes_key_expansion(key):
    # Key expansion logic to generate all round keys
    # ...
    return expanded_key
```

**Encryption and Decryption Functions:**
AES encryption and decryption use the above transformations in a sequence of rounds to ensure secure encryption.

```python
def aes_encrypt_block(plaintext, key):
    # AES block encryption process
    # ...
    return ciphertext

def aes_decrypt_block(ciphertext, key):
    # AES block decryption process
    # ...
    return plaintext
```

---

## Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/annlima/crypto-algorithms.git
   cd crypto-algorithms
   ```

2. Run the Python script for RC4 or AES encryption/decryption.

3. Example usage:
   ```python
   # RC4 Encryption
   key = b'secret_key'
   plaintext = b'Hello, World!'
   ciphertext = rc4_encrypt(plaintext, key)

   # AES Encryption (Assume AES class defined)
   aes = AES(key_size=128)
   ciphertext = aes.encrypt(plaintext, key)
   decrypted_text = aes.decrypt(ciphertext, key)
   ```

---

## Code Examples

### RC4 Example
```python
key = b'secret_key'
plaintext = b'This is a secret message'
ciphertext = rc4_encrypt(plaintext, key)
print("Ciphertext (hex):", ciphertext.hex())
decrypted_text = rc4_encrypt(ciphertext, key)  # Symmetric decryption
print("Decrypted text:", decrypted_text.decode('utf-8'))
```

### AES Example
```python
aes = AES(key_size=128)
key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
plaintext = b'This is a secret message'
ciphertext = aes.encrypt(plaintext, key)
print("Ciphertext (hex):", ciphertext.hex())
decrypted_text = aes.decrypt(ciphertext, key)
print("Decrypted text:", decrypted_text.decode('utf-8'))
```
