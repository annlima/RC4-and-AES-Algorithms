# AES Encryption and Decryption in Python

This repository provides a Python implementation of the Advanced Encryption Standard (AES) for data encryption and decryption. The AES algorithm is widely used for secure data transmission in symmetric key cryptography. This code includes support for 128, 192, and 256-bit keys and implements all essential AES transformations.

## Features

- **Complete AES Algorithm**: Implements the SubBytes, ShiftRows, MixColumns, and AddRoundKey transformations.
- **Key Expansion**: Generates round keys based on the initial cipher key.
- **Encryption & Decryption**: Encrypt and decrypt data in blocks of 128 bits (16 bytes).
- **Padding**: Includes PKCS#7 padding for handling non-block-size data.
- **Debugging Mode**: Optional debug mode for step-by-step output of internal states during encryption and decryption.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features Overview](#features-overview)
- [Example](#example)
- [License](#license)

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. This project requires no additional libraries.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/annlima/H4_Cybersecurity.git
   cd H4_Cybersecurity
   ```

2. Open the code in your preferred IDE or text editor.

## Usage

This AES implementation can be used to encrypt and decrypt messages with a specific key size. To start, create an instance of the `AES` class with the desired key size (128, 192, or 256 bits).

### Encryption and Decryption

- **Encrypt**: Use the `encrypt` method to encrypt a plaintext message with a specified key.
- **Decrypt**: Use the `decrypt` method to convert the ciphertext back to plaintext.

```python
from aes import AES

# Initialize AES with 128-bit key
aes = AES(key_size=128)
aes.set_debug(True)  # Enable debug mode for detailed output

# Define plaintext and key
plaintext = "This is a secret message."
key = b"mysecretkey12345"  # 16 bytes for AES-128

# Encrypt the plaintext
ciphertext = aes.encrypt(plaintext, key)
print(f"Ciphertext (hex): {ciphertext.hex()}")

# Decrypt the ciphertext
decrypted_plaintext = aes.decrypt(ciphertext, key)
print(f"Decrypted plaintext: {decrypted_plaintext.decode('utf-8')}")
```

## Project Structure

```
aes-python-encryption/
├── aes.py             # Main AES implementation
├── README.md          # Project documentation
└── example.py         # Example usage of AES encryption/decryption
```

## Features Overview

### 1. Key Expansion

The code generates a series of round keys from the initial cipher key, which are used in each round of encryption and decryption.

### 2. Encryption Steps

The encryption process includes:
- **AddRoundKey**: Initial XOR with the round key.
- **SubBytes**: Byte substitution using the S-Box.
- **ShiftRows**: Row-wise shifting.
- **MixColumns**: Column-wise mixing.
- **Final Round**: The last round omits the MixColumns step.

### 3. Decryption Steps

The decryption process includes:
- **Inverse ShiftRows**: Reverses the ShiftRows transformation.
- **Inverse SubBytes**: Reverses the byte substitution.
- **Inverse MixColumns**: Reverses column mixing.
- **AddRoundKey**: XOR with the appropriate round key.

### 4. PKCS#7 Padding

Handles data that does not fit exactly into 16-byte blocks, adding padding during encryption and removing it during decryption.

## Example

An example of using this AES implementation:

```python
# Encrypt a message
aes = AES(key_size=128)
key = b"mysecretkey12345"
ciphertext = aes.encrypt("Confidential Data", key)
print(f"Ciphertext: {ciphertext.hex()}")

# Decrypt the message
decrypted_message = aes.decrypt(ciphertext, key)
print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy using AES encryption and decryption! Contributions, issues, and pull requests are welcome to help improve this implementation.
