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

from net import test_input
from crypto import *

#####################################################
#                                                   #
#                      Fonctions                    #
#                                                   #
#####################################################

# # Fonction pour générer une clé de chiffrement et la stocker dans un fichier (si elle n'existe pas déjà)
# def generate_key():
#     if not os.path.exists("secret.key"):
#         key = Fernet.generate_key()
#         with open("secret.key", "wb") as key_file:
#             key_file.write(key)

# # Fonction pour charger la clé de chiffrement
# def load_key():
#     return open("secret.key", "rb").read()

# Load or generate the encryption key
key_filename = "secret.key"
if os.path.exists(key_filename):
    with open(key_filename, 'rb') as f:
        key = f.read()
else:
    key = generate_key()
    with open(key_filename, 'wb') as f:
        f.write(key)

# Fonction pour chiffrer un mot de passe
# def encrypt_password(password):
#     key = load_key()
#     f = Fernet(key)
#     encrypted_password = f.encrypt(password.encode())
#     return encrypted_password

# # Fonction pour enregistrer un mot de passe dans un fichier texte
# def save_password():
#     password = entry_password.get()

#     if password:
#         encrypted_password = encrypt_password(password)
#         with open("passwords.txt", "a") as f:
#             f.write(f" {encrypted_password.decode()}\n")
#         messagebox.showinfo("Succès", "Mot de passe enregistré avec succès !")
#         entry_password.delete(0, tk.END)
#     else:
#         messagebox.showwarning("Erreur", "Veuillez entrer un mot de passe.")

def show_generated_password():
    """Affiche le mot de passe généré et évalue sa force."""
    password = generate_password(random.randint(6,20))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    strength = test_input(password)
    strength_label.config(text=f"Force du mot de passe : {strength}")


#####################################################
#                                                   #
#                Database Fonctions                 #
#                                                   #
#####################################################

# Initialise la Base de Donnée
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
        
# Stocker les Mots de Passe
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
    
# Récupère un mot de Passe
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

# Sauvegarder un mot de passe
def save_password_ui():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if site and username and password:
        if not test_input(password) == "['fort']":
            messagebox.showwarning("Error", "Le mot de passe n'est pas assez fort. Veuillez choisir un mot de passe plus fort.")
            return
        encrypted_password = encrypt_password(key, password)
        store_password(site, username, encrypted_password)
        password_listbox.insert(tk.END, f"{site} ({username})")
        messagebox.showinfo("Success", f"Password for {site} saved.")
    else:
        messagebox.showwarning("Error", "Please enter a site, username, and password.")


# Recherche les Mots de Passe
def search_password():
    site = site_entry.get()
    username = username_entry.get()
    if site and username:
        encrypted_password = retrieve_password(site, username)
        if encrypted_password:
            password = decrypt_password(key, encrypted_password)
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
            messagebox.showinfo("Success", f"Password for {site} found.")
        else:
            messagebox.showwarning("Error", f"No password for {site} and {username}.")
    else:
        messagebox.showwarning("Error", "Please enter a site and username.")


# Exporte les mots de Passe
def export_passwords():
    file_name = simpledialog.askstring("Export", "Name of the file to export:")
    if file_name:
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('SELECT * FROM passwords')
        passwords = c.fetchall()
        conn.close()
        with open(file_name + '.json', 'w') as f:
            json.dump(passwords, f)
        messagebox.showinfo("Success", "Passwords successfully exported.")

# Importe les Mots de Passe
def import_passwords():
    file_name = simpledialog.askstring("Import", "Name of the file to import:")
    if file_name:
        try:
            with open(file_name + '.json', 'r') as f:
                imported_passwords = json.load(f)
                conn = sqlite3.connect('passwords.db')
                c = conn.cursor()
                for site, username, encrypted_password in imported_passwords:
                    c.execute('''
                        INSERT OR REPLACE INTO passwords (site, username, encrypted_password)
                        VALUES (?, ?, ?)
                    ''', (site, username, encrypted_password))
                conn.commit()
                conn.close()
                password_listbox.delete(0, tk.END)
                for site, username, _ in imported_passwords:
                    password_listbox.insert(tk.END, f"{site} ({username})")
                messagebox.showinfo("Success", "Passwords successfully imported.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during import: {str(e)}")

#####################################################
#                                                   #
#               Interface Utilisateur               #
#                                                   #
#####################################################

# Init la Database
initialize_db()

# Création de l'interface utilisateur
# generate_key()  # Génère la clé de chiffrement si elle n'existe pas encore

# Creation de la fenetre principal
root = tk.Tk()
root.title("Gestionnaire et Analyse de mots de passe")
root.geometry("800x600")

# Create a frame for the widgets
frame = tk.Frame(root, bg='#80c1ff', bd=3)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# Label et champ pour entrer le mot de passe
# label_password = tk.Label(root, text="Mot de passe :")
# label_password.pack(pady=5)
# entry_password = tk.Entry(root, show="*")
# entry_password.pack(pady=10)

# Entry field for the site
site_entry = tk.Entry(frame, font=('Oswald', 12))
site_entry.place(relwidth=0.2, relheight=1)
site_entry.insert(0, "Site")

# Entry field for the username
username_entry = tk.Entry(frame, font=('Oswald', 12))
username_entry.place(relx=0.25, relwidth=0.2, relheight=1)
username_entry.insert(0, "Username")

# Entry field for the password
password_entry = tk.Entry(frame, font=('Oswald', 12))
password_entry.place(relx=0.5, relwidth=0.2, relheight=1)
password_entry.insert(0, "Password")

# Label pour afficher la force du mot de passe
strength_label = tk.Label(root, text="")
strength_label.pack(pady=10)

# Bouton pour évaluer la force du mot de passe entré
evaluate_button = tk.Button(root, text="Évaluer la Force", command=lambda: strength_label.config(text=f"Force du mot de passe : {test_input(password_entry.get())}"))
evaluate_button.pack(pady=5)
evaluate_button.place(relx=0.25, rely=0.25, relheight=0.05, relwidth=0.5)

# Bouton pour générer un mot de passe aléatoire
generate_button = tk.Button(root, text="Générer un Mot de Passe", command=show_generated_password)
generate_button.pack(pady=10)
generate_button.place(relx=0.25, rely=0.35, relheight=0.05, relwidth=0.5)

# Bouton pour enregistrer le mot de passe
# button_save = tk.Button(root, text="Enregistrer", command=save_password_ui)
# button_save.pack(pady=20)

# Button to add a password
add_button = tk.Button(frame, text="Add", font=('Oswald', 12), command=save_password_ui)
add_button.place(relx=0.75, relheight=1, relwidth=0.2)

# Frame for the password listbox and scrollbar
password_frame = tk.Frame(root)
password_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.3, anchor='n')

# List of saved passwords
password_listbox = tk.Listbox(password_frame, font=('Oswald', 12))
password_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the password listbox
password_scrollbar = tk.Scrollbar(password_frame, orient=tk.VERTICAL)
password_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the listbox
password_listbox.config(yscrollcommand=password_scrollbar.set)
password_scrollbar.config(command=password_listbox.yview)

# Entry field for password search
search_entry = tk.Entry(root, font=('Oswald', 12))
search_entry.place(relx=0.5, rely=0.85, relwidth=0.65, anchor='n')

# Button to search for a password
search_button = tk.Button(root, text="Search", font=('Oswald', 12), command=search_password)
search_button.place(relx=0.85, rely=0.85, anchor='n')

# Navigation menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export", command=export_passwords)
file_menu.add_command(label="Import", command=import_passwords)
file_menu.add_command(label="Quit", command=root.quit)

# Load existing passwords into the list
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('SELECT site, username FROM passwords')
for site, username in c.fetchall():
    password_listbox.insert(tk.END, f"{site} ({username})")
conn.close()

# Lancer l'application Tkinter
root.mainloop()
