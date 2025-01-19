from cryptography.fernet import Fernet

def generate_key():
    """
    Génère une clé de chiffrement.

    Returns:
        bytes: La clé de chiffrement.
    """
    return Fernet.generate_key()

def encrypt_password(key, password):
    """
    Chiffre un mot de passe.

    Args:
        key (bytes): La clé de chiffrement.
        password (str): Le mot de passe à chiffrer.

    Returns:
        bytes: Le mot de passe chiffré.
    """
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(key, encrypted_password):
    """
    Déchiffre un mot de passe.

    Args:
        key (bytes): La clé de chiffrement.
        encrypted_password (bytes): Le mot de passe chiffré.

    Returns:
        str: Le mot de passe déchiffré.
    """
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()