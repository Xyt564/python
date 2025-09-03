import customtkinter as ctk
from cryptography.fernet import Fernet
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "vault.json")
KEY_FILE = os.path.join(BASE_DIR, "key.key")


# ------------------ Encryption ------------------

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

fernet = Fernet(load_key())

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

# ------------------ File Handling ------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

# ------------------ GUI ------------------

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("500x500")

        self.site_entry = ctk.CTkEntry(self, placeholder_text="Site")
        self.site_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.add_button = ctk.CTkButton(self, text="Add", command=self.add_password)
        self.add_button.pack(pady=10)

        self.show_button = ctk.CTkButton(self, text="Show Saved", command=self.show_passwords)
        self.show_button.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=400, height=200)
        self.output_box.pack(pady=20)

    def add_password(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (site and username and password):
            self.output_box.insert("end", "❗ All fields are required.\n")
            return

        encrypted = encrypt_password(password)
        data = load_data()
        data.append({"site": site, "username": username, "password": encrypted})
        save_data(data)

        self.output_box.insert("end", f"✅ Added {site}\n")
        self.site_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def show_passwords(self):
        self.output_box.delete("1.0", "end")
        data = load_data()
        if not data:
            self.output_box.insert("end", "No passwords saved yet.\n")
            return
        for item in data:
            try:
                decrypted = decrypt_password(item['password'])
                self.output_box.insert("end", f"{item['site']} | {item['username']} | {decrypted}\n")
            except Exception as e:
                self.output_box.insert("end", f"{item['site']} | {item['username']} | [DECRYPTION ERROR]\n")

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
