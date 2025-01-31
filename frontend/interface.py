import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

# Fonction pour générer une clé de chiffrement et la stocker dans un fichier (si elle n'existe pas déjà)
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

# Fonction pour charger la clé de chiffrement
def load_key():
    return open("secret.key", "rb").read()

# Fonction pour chiffrer un mot de passe
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Fonction pour enregistrer un mot de passe dans un fichier texte
def save_password():
    password = entry_password.get()

    if password:
        encrypted_password = encrypt_password(password)
        with open("passwords.txt", "a") as f:
            f.write(f" {encrypted_password.decode()}\n")
        messagebox.showinfo("Succès", "Mot de passe enregistré avec succès !")
        entry_password.delete(0, tk.END)
    else:
        messagebox.showwarning("Erreur", "Veuillez entrer un mot de passe.")

# Création de l'interface utilisateur
generate_key()  # Génère la clé de chiffrement si elle n'existe pas encore

root = tk.Tk()
root.title("Gestionnaire de mots de passe")

# Label et champ pour entrer le mot de passe
label_password = tk.Label(root, text="Mot de passe :")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Bouton pour enregistrer le mot de passe
button_save = tk.Button(root, text="Enregistrer", command=save_password)
button_save.pack(pady=20)

# Lancer l'application Tkinter
root.mainloop()
