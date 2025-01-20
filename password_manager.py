import sqlite3
import re

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def save_password(site, username, password):
    if not is_strong_password(password):
        print("The password is not strong enough. Please choose a stronger password.")
        return

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (site TEXT, username TEXT, encrypted_password TEXT)''')
    c.execute('INSERT INTO passwords (site, username, encrypted_password) VALUES (?, ?, ?)',
              (site, username, password))  # Vous pouvez ajouter un chiffrement ici
    conn.commit()
    conn.close()
    print("Password saved successfully.")
    
def display_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('SELECT site, username, encrypted_password FROM passwords')
    passwords = c.fetchall()
    conn.close()
    for site, username, encrypted_password in passwords:
        print(f"Site: {site}, Username: {username}, Encrypted Password: {encrypted_password}")

if __name__ == "__main__":
    # Exemple d'utilisation
    save_password("example.com", "user1", "WeakPass")
    save_password("example.com", "user2", "StrongPass1!")
    display_passwords()