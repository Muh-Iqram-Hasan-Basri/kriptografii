import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

def generate_key_from_password(password: str) -> bytes:
    # Mengubah password text menjadi kunci 256-bit (32 bytes) menggunakan SHA-256
    hash_obj = SHA256.new(password.encode('utf-8'))
    return hash_obj.digest()

def encrypt_file(input_filename: str, output_filename: str, password: str):
    key = generate_key_from_password(password)
    
    # Membaca file asli
    with open(input_filename, 'rb') as f:
        plaintext = f.read()
    
    # Membuat cipher AES dengan mode CBC
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv # Mengambil Initialization Vector (16 bytes)
    
    # Melakukan padding dan enkripsi
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    # Menyimpan IV dan ciphertext ke file baru
    with open(output_filename, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)
    print(f"[+] File '{input_filename}' berhasil dienkripsi menjadi '{output_filename}'")

def decrypt_file(input_filename: str, output_filename: str, password: str):
    key = generate_key_from_password(password)
    
    # Membaca file terenkripsi
    with open(input_filename, 'rb') as f:
        iv = f.read(16) # 16 bytes pertama adalah IV
        ciphertext = f.read()
        
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    try:
        # Dekripsi dan hapus padding
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, AES.block_size)
        
        with open(output_filename, 'wb') as f:
            f.write(plaintext)
        print(f"[+] File '{input_filename}' berhasil didekripsi menjadi '{output_filename}'")
    except (ValueError, KeyError):
        print("[-] Gagal dekripsi! Password salah atau file rusak.")

# --- BAGIAN UNTUK MENJALANKAN OTOMATIS ---
if __name__ == "__main__":
    file_target = "tugas_rahasia.txt"
    file_hasil_enkripsi = "tugas_rahasia.enc"
    file_hasil_dekripsi = "tugas_pulih.txt"
    password_anda = "IniPasswordAman123"

    # 1. Membuat file TXT dummy otomatis untuk bahan uji coba
    with open(file_target, "w", encoding="utf-8") as f:
        f.write("Halo Bu Desi, ini adalah isi file TXT asli sebelum dienkripsi menggunakan AES.")
    print(f"[!] File contoh '{file_target}' telah dibuat otomatis.")
    print("-" * 50)

    # 2. Jalankan Fungsi Enkripsi
    encrypt_file(file_target, file_hasil_enkripsi, password_anda)

    # 3. Jalankan Fungsi Dekripsi
    decrypt_file(file_hasil_enkripsi, file_hasil_dekripsi, password_anda)