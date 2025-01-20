import sqlite3

def display_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('SELECT site, username, encrypted_password FROM passwords')
    passwords = c.fetchall()
    conn.close()
    for site, username, encrypted_password in passwords:
        print(f"Site: {site}, Username: {username}, Encrypted Password: {encrypted_password}")

if __name__ == "__main__":
    display_passwords()
