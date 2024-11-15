import os
from typing import List, Union

# Define the AES S-Box
S_BOX = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16],
]

# Define the Inverse AES S-Box
INV_S_BOX = [
    [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
    [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
    [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
    [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
    [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
    [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
    [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0x3A, 0x45, 0x06],
    [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
    [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
    [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
    [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
    [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
    [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
    [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
    [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D],
]

RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]


def hex_matrix(matrix):
    """Convert a 4x4 matrix to hexadecimal string representation."""
    return [[f"{byte:02x}" for byte in row] for row in matrix]


class AES:
    def __init__(self, key_size: int = 128):
        """Initialize AES with key size (128, 192, or 256 bits)."""
        if key_size not in (128, 192, 256):
            raise ValueError("Key size must be 128, 192, or 256 bits")
        self.key_size = key_size
        self.rounds = {128: 10, 192: 12, 256: 14}[key_size]
        self.S_BOX = S_BOX
        self.INV_S_BOX = INV_S_BOX
        self.RCON = RCON
        self.debug = False  # Add debug flag

    def set_debug(self, debug: bool):
        """Enable or disable debug output."""
        self.debug = debug

    def _debug_print(self, *args, **kwargs):
        """Print debug information if debug mode is enabled."""
        if self.debug:
            print(*args, **kwargs)

    def encrypt(self, plaintext: Union[bytes, str], key: Union[bytes, str]) -> bytes:
        # Ensure plaintext is bytes
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        # Ensure key is in correct bytes format
        if isinstance(key, str):
            key = bytes.fromhex(key) if all(c in '0123456789abcdefABCDEF' for c in key) else key.encode('utf-8')

        # Validate key length
        if len(key) * 8 != self.key_size:
            raise ValueError(f"Key must be {self.key_size} bits")

        # Pad the plaintext
        padded_text = self._pad_pkcs7(plaintext)
        self._debug_print(f"Padded text (hex): {padded_text.hex()}")

        # Encrypt each block
        blocks = [padded_text[i:i + 16] for i in range(0, len(padded_text), 16)]
        ciphertext = b''
        for block in blocks:
            encrypted_block = self._encrypt_block(block, key)
            self._debug_print(f"Encrypted block (hex): {encrypted_block.hex()}")
            ciphertext += encrypted_block

        return ciphertext

    def decrypt(self, ciphertext: bytes, key: Union[bytes, str]) -> bytes:
        # Convert key to bytes if necessary
        if isinstance(key, str):
            key = bytes.fromhex(key) if all(c in '0123456789abcdefABCDEF' for c in key) else key.encode('utf-8')

        # Validate ciphertext length
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16 bytes")

        # Decrypt each block and assemble plaintext
        blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
        plaintext = b''

        for block in blocks:
            decrypted_block = self._decrypt_block(block, key)
            self._debug_print(f"Decrypted block (hex): {decrypted_block.hex()}")
            plaintext += decrypted_block

        # Unpad and return plaintext
        try:
            unpadded_plaintext = self._unpad_pkcs7(plaintext)
            self._debug_print(f"Unpadded plaintext (hex): {unpadded_plaintext.hex()}")
            return unpadded_plaintext
        except ValueError as e:
            self._debug_print(f"Padding error: {str(e)}")
            raise

    # PKCS#7 padding and unpadding functions

    def _pad_pkcs7(self, data: bytes) -> bytes:
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        print(f"Padding added: {padding.hex()}")
        return data + padding

    def _unpad_pkcs7(self, data: bytes) -> bytes:
        if not data:
            raise ValueError("Data cannot be empty")
        padding_length = data[-1]
        if padding_length < 1 or padding_length > 16:
            raise ValueError("Invalid padding length")
        if data[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Inconsistent padding bytes detected during unpadding")
        return data[:-padding_length]


    # Encrypting a single block function
    def _encrypt_block(self, plaintext: bytes, key: bytes) -> bytes:
        # Initialize the state and expand the key
        state = [[plaintext[i * 4 + j] for j in range(4)] for i in range(4)]
        expanded_key = self.key_expansion(key)

        # Perform encryption steps
        self.add_round_key(state, expanded_key[:4])  # Initial AddRoundKey
        for round in range(1, self.rounds):
            self.sub_bytes(state)
            self.shift_rows(state)
            self.mix_columns(state)
            self.add_round_key(state, expanded_key[round * 4:(round + 1) * 4])
        # Final round (no MixColumns)
        self.sub_bytes(state)
        self.shift_rows(state)
        self.add_round_key(state, expanded_key[self.rounds * 4:])
        return bytes(state[i][j] for i in range(4) for j in range(4))

    # Decryption block function
    def _decrypt_block(self, ciphertext: bytes, key: bytes) -> bytes:
        # Decryption steps
        state = [[ciphertext[i * 4 + j] for j in range(4)] for i in range(4)]
        expanded_key = self.key_expansion(key)

        self.add_round_key(state, expanded_key[self.rounds * 4:])
        for round in range(self.rounds - 1, 0, -1):
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
            self.add_round_key(state, expanded_key[round * 4:(round + 1) * 4])
            self._inv_mix_columns(state)

        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)
        self.add_round_key(state, expanded_key[:4])
        return bytes(state[i][j] for i in range(4) for j in range(4))

    @staticmethod
    def add_round_key(state, round_key):
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i][j]
        print(f"State after AddRoundKey: {hex_matrix(state)}")

    def sub_bytes(self, state):
        for i in range(4):
            for j in range(4):
                byte = state[i][j]
                state[i][j] = self.S_BOX[byte >> 4][byte & 0x0F]

    def key_expansion(self, key: bytes) -> List[List[int]]:
        expanded_key = [list(key[i:i + 4]) for i in range(0, len(key), 4)]
        for i in range(4, 4 * (self.rounds + 1)):
            temp = expanded_key[i - 1]
            if i % 4 == 0:
                temp = [self.S_BOX[b >> 4][b & 0x0F] for b in temp[1:] + temp[:1]]
                temp[0] ^= self.RCON[i // 4 - 1]
            expanded_key.append([expanded_key[i - 4][j] ^ temp[j] for j in range(4)])
        return expanded_key

    @staticmethod
    def shift_rows(state):
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]

    def mix_columns(self, state):
        for i in range(4):
            a = state[i][:]
            state[i][0] = self.gf_mul(a[0], 2) ^ self.gf_mul(a[1], 3) ^ a[2] ^ a[3]
            state[i][1] = a[0] ^ self.gf_mul(a[1], 2) ^ self.gf_mul(a[2], 3) ^ a[3]
            state[i][2] = a[0] ^ a[1] ^ self.gf_mul(a[2], 2) ^ self.gf_mul(a[3], 3)
            state[i][3] = self.gf_mul(a[0], 3) ^ a[1] ^ a[2] ^ self.gf_mul(a[3], 2)
        print(f"State after MixColumns: {hex_matrix(state)}")

    @staticmethod
    def gf_mul(a, b):
        result = 0
        for i in range(8):
            if b & 1:
                result ^= a
            high_bit = a & 0x80
            a = (a << 1) & 0xFF
            if high_bit:
                a ^= 0x1B
            b >>= 1
        return result

    def _inv_sub_bytes(self, state: List[List[int]]) -> None:
        """Apply inverse S-Box substitution."""
        for i in range(4):
            for j in range(4):
                byte = state[i][j]
                state[i][j] = self.INV_S_BOX[byte >> 4][byte & 0x0F]

    @staticmethod
    def _inv_shift_rows(state: List[List[int]]) -> None:
        """Inverse shift rows transformation."""
        state[1] = state[1][-1:] + state[1][:-1]
        state[2] = state[2][-2:] + state[2][:-2]
        state[3] = state[3][-3:] + state[3][:-3]

    def _inv_mix_columns(self, state: List[List[int]]) -> None:
        """Inverse mix columns transformation."""
        for i in range(4):
            a = state[i][:]
            state[i][0] = self.gf_mul(0x0E, a[0]) ^ self.gf_mul(0x0B, a[1]) ^ self.gf_mul(0x0D, a[2]) ^ self.gf_mul(
                0x09, a[3])
            state[i][1] = self.gf_mul(0x09, a[0]) ^ self.gf_mul(0x0E, a[1]) ^ self.gf_mul(0x0B, a[2]) ^ self.gf_mul(
                0x0D, a[3])
            state[i][2] = self.gf_mul(0x0D, a[0]) ^ self.gf_mul(0x09, a[1]) ^ self.gf_mul(0x0E, a[2]) ^ self.gf_mul(
                0x0B, a[3])
            state[i][3] = self.gf_mul(0x0B, a[0]) ^ self.gf_mul(0x0D, a[1]) ^ self.gf_mul(0x09, a[2]) ^ self.gf_mul(
                0x0E, a[3])

    @staticmethod
    def generate_key(key_size=128):
        return os.urandom(key_size // 8)
