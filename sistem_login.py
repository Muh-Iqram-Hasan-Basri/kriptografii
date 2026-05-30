import hashlib
import json
import os

# Nama file untuk penyimpanan data user (Format: JSON)
DATA_FILE = "users_db.json"

def load_data():
    """Memuat data user dari file JSON"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    """Menyimpan data user ke file JSON"""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def hash_password(password, algorithm):
    """Melakukan hashing password berdasarkan algoritma yang dipilih"""
    if algorithm == "MD5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "SHA-256":
        return hashlib.sha256(password.encode()).hexdigest()
    return None

def registrasi_akun():
    print("\n=== MENU REGISTRASI AKUN ===")
    username = input("Masukkan Username baru: ").strip()
    
    users = load_data()
    if username in users:
        print("❌ Gagal: Username sudah terdaftar!")
        return

    password_asli = input("Masukkan Password: ")
    
    print("\nPilih Algoritma Hashing:")
    print("1. MD5")
    print("2. SHA-256")
    pilihan = input("Pilih (1/2): ")
    
    if pilihan == "1":
        algo = "MD5"
    elif pilihan == "2":
        algo = "SHA-256"
    else:
        print("❌ Pilihan tidak valid!")
        return

    # Proses Hashing
    password_terhash = hash_password(password_asli, algo)
    
    # Simpan ke 'database' JSON
    users[username] = {
        "hashed_password": password_terhash,
        "algorithm": algo
    }
    save_data(users)
    
    # OUTPUT SESUAI KETENTUAN SOAL
    print("\n--- OUTPUT REGISTRASI ---")
    print(f"✔ Username     : {username}")
    print(f"✔ Password Asli: {password_asli}")
    print(f"✔ Algoritma    : {algo}")
    print(f"✔ Hasil Hash   : {password_terhash}")
    print("-------------------------")
    print("🎉 Akun berhasil didaftarkan!")

def login_pengguna():
    print("\n=== MENU LOGIN PENGGUNA ===")
    username = input("Username: ").strip()
    password_input = input("Password: ")
    
    users = load_data()
    
    if username not in users:
        print("❌ Gagal: Username tidak ditemukan!")
        return
    
    # Ambil data dari database
    user_data = users[username]
    hash_tersimpan = user_data["hashed_password"]
    algo_digunakan = user_data["algorithm"]
    
    # Proses hashing pada password yang diinput saat login
    hash_input = hash_password(password_input, algo_digunakan)
    
    # OUTPUT PROSES VERIFIKASI SESUAI KETENTUAN SOAL
    print("\n--- PROSES VERIFIKASI LOGIN ---")
    print(f"1. Algoritma yang digunakan database : {algo_digunakan}")
    print(f"2. Hash yang tersimpan di database   : {hash_tersimpan}")
    print(f"3. Hasil hash dari password input    : {hash_input}")
    
    # Mencocokkan nilai hash
    if hash_input == hash_tersimpan:
        print("\n=> STATUS: MATCH (Hash Cocok)")
        print("--------------------------------")
        print(f"🔒 Selamat datang, {username}! Login BERHASIL.")
    else:
        print("\n=> STATUS: MISMATCH (Hash Berbeda)")
        print("--------------------------------")
        print("❌ Login GAGAL! Password salah.")

def main():
    while True:
        print("\n=================================")
        print("  SISTEM LOGIN SECURE WITH HASH  ")
        print("=================================")
        print("1. Registrasi Akun")
        print("2. Login Pengguna")
        print("3. Keluar")
        pilihan = input("Pilihan Menu (1/2/3): ")
        
        if pilihan == "1":
            registrasi_akun()
        elif pilihan == "2":
            login_pengguna()
        elif pilihan == "3":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia. Silakan coba lagi.")

if __name__ == "__main__":
    main()