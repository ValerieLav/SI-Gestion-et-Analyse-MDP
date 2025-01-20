import json
import os

def store_password(site, username, encrypted_password, filename="passwords.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            passwords = json.load(f)
    else:
        passwords = {}

    if site not in passwords:
        passwords[site] = {}

    # Vérifier si encrypted_password est de type bytes
    if isinstance(encrypted_password, bytes):
        encrypted_password = encrypted_password.decode()

    passwords[site][username] = encrypted_password

    with open(filename, 'w') as f:
        json.dump(passwords, f)

def retrieve_password(site, username, filename="passwords.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            passwords = json.load(f)
        if site in passwords and username in passwords[site]:
            return passwords[site][username]
    return None

def store_passwords(passwords, filename="passwords.json"):
    with open(filename, 'w') as f:
        json.dump(passwords, f)

def load_passwords(filename="passwords.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}