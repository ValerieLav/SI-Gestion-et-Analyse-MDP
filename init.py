#####################################################
#                                                   #
#              Importer les Librairies              #
#                                                   #
#####################################################

import os
import random
import sqlite3

import tkinter as tk
from tkinter import messagebox, simpledialog

from cryptography.fernet import Fernet


from gen_mdp import *

# import nbformat
# from IPython.core.interactiveshell import InteractiveShell
#
# def run_notebook(notebook_path):
#     with open(notebook_path, "r", encoding="utf-8") as f:
#         notebook = nbformat.read(f, as_version=4)

#     shell = InteractiveShell.instance()
#     for cell in notebook.cells:
#         if cell.cell_type == "code":
#             shell.run_cell(cell.source)

# # Example: Execute the notebook
# run_notebook("net.ipynb")

from net import *

#####################################################
#                                                   #
#                      Database                     #
#                                                   #
#####################################################

# Initialize the database
def initialize_db():
    db_path = 'passwords.db'
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('SELECT name FROM sqlite_master WHERE type="table"')
            conn.close()
        except sqlite3.DatabaseError:
            os.remove(db_path)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    PRIMARY KEY (site, username)
                )
            ''')
            conn.commit()
            conn.close()
    else:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                site TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                PRIMARY KEY (site, username)
            )
        ''')
        conn.commit()
        conn.close()
        
# Function to store a password
def store_password(site, username, encrypted_password):
    # Vérifier si encrypted_password est de type bytes
    if isinstance(encrypted_password, bytes):
        encrypted_password = encrypted_password.decode()

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO passwords (site, username, encrypted_password)
        VALUES (?, ?, ?)
    ''', (site, username, encrypted_password))
    conn.commit()
    conn.close()
    
# Function to retrieve a password
def retrieve_password(site, username):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        SELECT encrypted_password FROM passwords
        WHERE site = ? AND username = ?
    ''', (site, username))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

#####################################################
#                                                   #
#                      Fonctions                    #
#                                                   #
#####################################################

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

def show_generated_password():
    """Affiche le mot de passe généré et évalue sa force."""
    password = generate_password(random.randint(6,20))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    strength = test_input(password)
    strength_label.config(text=f"Force du mot de passe : {strength}")

#####################################################
#                                                   #
#               Interface Utilisateur               #
#                                                   #
#####################################################

# Initialize the database
initialize_db()

# Création de l'interface utilisateur
generate_key()  # Génère la clé de chiffrement si elle n'existe pas encore

root = tk.Tk()
root.title("Gestionnaire de mots de passe")
root.geometry("800x600")

# Label et champ pour entrer le mot de passe
label_password = tk.Label(root, text="Mot de passe :")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

# Label pour afficher la force du mot de passe
strength_label = tk.Label(root, text="")
strength_label.pack(pady=10)

# Bouton pour évaluer la force du mot de passe entré
evaluate_button = tk.Button(root, text="Évaluer la Force", command=lambda: strength_label.config(text=f"Force du mot de passe : {test_input(entry_password.get())}"))
evaluate_button.pack(pady=5)

# Bouton pour générer un mot de passe aléatoire
generate_button = tk.Button(root, text="Générer un Mot de Passe", command=show_generated_password)
generate_button.pack(pady=10)

# Bouton pour enregistrer le mot de passe
button_save = tk.Button(root, text="Enregistrer", command=save_password)
button_save.pack(pady=20)

# Lancer l'application Tkinter
root.mainloop()
