import os
from AES import AES
from RC4 import rc4_encrypt

def main():
    # Initialize AES with a 128-bit key
    aes = AES(key_size=128)
    aes.set_debug(True)  # Enable debug output

    # Define plaintext and key
    plaintext = "This is a secret message."
    key = b"mysecretkey12345"  # 16 bytes for AES-128

    # Ensure the key length matches the AES key size
    if len(key) * 8 != aes.key_size:
        raise ValueError(f"Key must be {aes.key_size // 8} bytes for AES-{aes.key_size}.")

    # Encrypt the plaintext
    ciphertext = aes.encrypt(plaintext, key)
    print(f"Ciphertext (hex): {ciphertext.hex()}")

    # Decrypt the ciphertext
    decrypted_plaintext = aes.decrypt(ciphertext, key)
    print(f"Decrypted plaintext: {decrypted_plaintext.decode('utf-8')}")

    plaintext = b"This is a secret message."
    key = b"myrc4secretkey"
    ciphertext = rc4_encrypt(plaintext, key)
    print(f"RC4 Ciphertext (hex): {ciphertext.hex()}")
    decrypted = rc4_encrypt(ciphertext, key)  # RC4 is symmetric
    print(f"RC4 Decrypted plaintext: {decrypted.decode('utf-8')}")

if __name__ == "__main__":
    main()
