from AES import AES, os

# Create an AES instance with a 128-bit key
aes = AES(key_size=128)

# Enable debug mode if you want to see intermediate states
aes.set_debug(True)

# Generate a random key (or you can define your own)
key = aes.generate_key(key_size=128)
print(f"Generated Key (hex): {key.hex()}")

# Define the plaintext message you want to encrypt
plaintext = "Hello, AES encryption!"

# Encrypt the plaintext
ciphertext = aes.encrypt(plaintext, key)
print(f"Ciphertext (hex): {ciphertext.hex()}")

# Decrypt the ciphertext
decrypted_text = aes.decrypt(ciphertext, key)
print(f"Decrypted Text: {decrypted_text.decode('utf-8')}")
