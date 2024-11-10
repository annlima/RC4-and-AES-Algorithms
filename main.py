from AES import AES, os
from RC4 import rc4_encrypt
# Instantiate the AES object with 128-bit key size
aes = AES(key_size=128)

# Generate a 128-bit key (16 bytes)
key = aes.generate_key(key_size=128)

# Define an initialization vector (IV) if needed, or use it directly
iv = os.urandom(16)  # optional if you want to use CBC mode encryption

# Define your plaintext
plaintext = "This is a secret message"

# Encrypt the plaintext
ciphertext = aes.encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext.hex()}")

# Decrypt the ciphertext
decrypted_text = aes.decrypt(ciphertext, key)
print("Decrypted bytes:", decrypted_text)
try:
    print("Decrypted text:", decrypted_text.decode('utf-8'))
except UnicodeDecodeError:
    print("The decrypted bytes do not represent valid UTF-8 text.")
