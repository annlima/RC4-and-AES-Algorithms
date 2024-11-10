import hashlib
import binascii
from typing import Tuple, List
import RC4
from AES import AES
import os

# Display decrypted results safely
def safe_decode(data: bytes) -> str:
    try:
        # Strip potential padding bytes for display purposes
        data = data.rstrip(b'\x00').rstrip(b'\x01').rstrip(b'\x02').rstrip(b'\x03').rstrip(b'\x04').rstrip(b'\x05').rstrip(b'\x06').rstrip(b'\x07').rstrip(b'\x08')
        return data.decode('utf-8')
    except UnicodeDecodeError:
        print(f"Warning: Non-UTF-8 bytes detected in: {data.hex()}")
        return data.hex()  # Fallback to hex representation

def combined_rc4_aes_encrypt(plaintext: bytes, rc4_key: bytes, aes_key: bytes) -> bytes:
    """Encrypts plaintext using RC4, then AES."""
    rc4_encrypted = RC4.rc4_encrypt(plaintext, rc4_key)
    aes = AES(key_size=128)
    aes_encrypted = aes.encrypt(rc4_encrypted, aes_key)
    return aes_encrypted


def read_text_file(file_path):
    """Reads and returns the content of a .txt file as bytes, removing trailing newlines and spaces."""
    try:
        with open(file_path, 'rb') as file:  # Open in binary mode
            content = file.read().rstrip(b'\n').rstrip()  # Trim trailing newlines and spaces
        return content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_avalanche_effect(cipher1: bytes, cipher2: bytes) -> float:
    """Calculates the avalanche effect between two ciphertexts."""
    bit_diff = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(cipher1, cipher2))
    total_bits = len(cipher1) * 8
    return (bit_diff / total_bits) * 100

def modify_key(key: bytes, modifications: List[Tuple[int, str]]) -> List[bytes]:
    """Modifies the key at specified positions with given characters."""
    modified_keys = []
    for pos, char in modifications:
        key_list = list(key)
        key_list[pos] = ord(char)  # Ensure the character is represented as its byte value
        modified_keys.append(bytes(key_list))  # Convert the list back to bytes
    return modified_keys

def analyze_files(file1_path: str, file2_path: str, aes_key: bytes, rc4_key: bytes, aes_modifications: List[Tuple[int, str]], rc4_modifications: List[Tuple[int, str]]) -> None:
    # Initialize AES with a 128-bit key
    aes = AES(key_size=128)
    aes.set_debug(True)  # Enable debug output

    # Ensure the key length matches the AES key size
    if len(aes_key) * 8 != aes.key_size:
        raise ValueError(f"Key must be {aes.key_size // 8} bytes for AES-{aes.key_size}.")

    """Analyzes two files and reports the avalanche effect for AES and RC4 encryption."""
    # Read and pad files
    file1 = read_text_file(file1_path)
    print("Plaintext - File 2: ", file1)
    file2 = read_text_file(file2_path)
    print("Plaintext - File 2: ", file2)

    # Encrypt both and decrypt files with AES
    aes_cipher1 = aes.encrypt(file1, aes_key)
    aes_plaintext1 = aes.decrypt(aes_cipher1, aes_key)

    aes_cipher2 = aes.encrypt(file2, aes_key)
    aes_plaintext2 = aes.decrypt(aes_cipher2, aes_key)
    
    # Encrypt both files with RC4
    rc4_cipher1 = RC4.rc4_encrypt(file1, rc4_key)    
    rc4_plaintext1 = RC4.rc4_encrypt(rc4_cipher1, rc4_key)  # RC4 is symmetric

    rc4_cipher2 = RC4.rc4_encrypt(file2, rc4_key)
    rc4_plaintext2 = RC4.rc4_encrypt(rc4_cipher2, rc4_key)  # RC4 is symmetric

    # Encrypt using RC4-AES combination
    rc4_aes_cipher1 = combined_rc4_aes_encrypt(file1, rc4_key, aes_key)
    rc4_aes_cipher2 = combined_rc4_aes_encrypt(file2, rc4_key, aes_key)

    print("\nORIGINAL KEY RESULTS")

    print(f"AES Ciphertext - File 1 (hex): {aes_cipher1.hex()}")
    print(f"Decrypted plaintext - File 1: {safe_decode(aes_plaintext1)}")

    print(f"AES Ciphertext - File 2 (hex): {aes_cipher2.hex()}")
    print(f"Decrypted plaintext - File 2: {safe_decode(aes_plaintext2)}")

    print(f"RC4 Ciphertext - File 1 (hex): {rc4_cipher1.hex()}")
    print(f"RC4 Decrypted plaintext: {safe_decode(rc4_plaintext1)}")

    print(f"RC4 Ciphertext - File 2 (hex): {rc4_aes_cipher2.hex()}")
    print(f"RC4 Decrypted plaintext: {safe_decode(rc4_plaintext2)} \n")

    # Modify keys and perform analysis
    modified_aes_keys = modify_key(aes_key, aes_modifications)
    modified_rc4_keys = modify_key(rc4_key, rc4_modifications)

    
    for i, (mod_aes_key, mod_rc4_key) in enumerate(zip(modified_aes_keys, modified_rc4_keys)):
        # AES Analysis
        aes_cipher1_modified = aes.encrypt(file1, mod_aes_key)
        aes_avalanche1 = calculate_avalanche_effect(aes_cipher1, aes_cipher1_modified)
        
        aes_cipher2_modified = aes.encrypt(file2, mod_aes_key)
        aes_avalanche2 = calculate_avalanche_effect(aes_cipher2, aes_cipher2_modified)
        
        # RC4 Analysis
        rc4_cipher1_modified = RC4.rc4_encrypt(file1, mod_rc4_key)
        rc4_avalanche1 = calculate_avalanche_effect(rc4_cipher1, rc4_cipher1_modified)
        
        rc4_cipher2_modified = RC4.rc4_encrypt(file2, mod_rc4_key)
        rc4_avalanche2 = calculate_avalanche_effect(rc4_cipher2, rc4_cipher2_modified)
        
        # RC4-AES Analysis
        rc4_aes_cipher1_modified = combined_rc4_aes_encrypt(file1, mod_rc4_key, mod_aes_key)
        rc4_aes_avalanche1 = calculate_avalanche_effect(rc4_aes_cipher1, rc4_aes_cipher1_modified)
        
        rc4_aes_cipher2_modified = combined_rc4_aes_encrypt(file2, mod_rc4_key, mod_aes_key)
        rc4_aes_avalanche2 = calculate_avalanche_effect(rc4_aes_cipher2, rc4_aes_cipher2_modified)

        print("\nAVALANCHE EFFECT ANALYSIS WITH MODIFIED KEYS")
        # Print results for each modification
        print(f"\nModification {i+1} - AES Avalanche Effect (File 1): {aes_avalanche1:.2f}%")
        print(f"Modification {i+1} - AES Avalanche Effect (File 2): {aes_avalanche2:.2f}%")
        print(f"Modification {i+1} - RC4 Avalanche Effect (File 1): {rc4_avalanche1:.2f}%")
        print(f"Modification {i+1} - RC4 Avalanche Effect (File 2): {rc4_avalanche2:.2f}%")
        print(f"Modification {i+1} - RC4-AES Avalanche Effect (File 1): {rc4_aes_avalanche1:.2f}%")
        print(f"Modification {i+1} - RC4-AES Avalanche Effect (File 2): {rc4_aes_avalanche2:.2f}% \n")


