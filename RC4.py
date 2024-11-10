def rc4_key_scheduling(key):
    """Key scheduling algorithm for RC4."""
    key_length = len(key)
    S = list(range(256))  # Initial permutation of 256 bytes
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # Swap
    return S

def rc4_pseudo_random_generation(S, plaintext_length):
    """Generate keystream for encryption/decryption."""
    i = j = 0
    keystream = []
    for _ in range(plaintext_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # Swap
        keystream.append(S[(S[i] + S[j]) % 256])
    return keystream

def rc4_encrypt(plaintext, key):
    """Encrypt plaintext using RC4."""
    S = rc4_key_scheduling(key)
    keystream = rc4_pseudo_random_generation(S, len(plaintext))
    ciphertext = bytes([plaintext[i] ^ keystream[i] for i in range(len(plaintext))])
    return ciphertext
