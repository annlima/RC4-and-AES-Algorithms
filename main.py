import os
from AES import AES
from RC4 import rc4_encrypt
from AvalancheAnalysis import analyze_files

        
def main():
    # Define original keys
    aes_key = b"mysecretkey12345"  # 16 bytes for AES-128
    rc4_key = b"myrc4secretkey"

    #Key modifications 
    aes_modifications = [(0, 'n'), (2, 'z'), (9, 'l')]  # mysecretkey12345 -> nysectretkey12345 -> myzecretkey12345 -> mysecretley12345
    rc4_modifications = [(0, 'n'), (4, '5'), (10, 'u')]  # myrc4secretkey -> nyrc4secretkey -> myrc5secretkey -> myrc4secreukey

    #Encrypt, decrypt, and analyze
    analyze_files("File1.txt", "File3.pdf", aes_key, rc4_key, aes_modifications, rc4_modifications)

    
if __name__ == "__main__":
    main()
