import os
import json
import random
import string
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import net  # Importation du module net.py

# Fonction pour générer un mot de passe aléatoire
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    strength = check_password_strength(password)
    strength_label.config(text=f"Strength of password : {strength}")

# Fonction pour vérifier la force du mot de passe (en utilisant la fonction de net.py si disponible)
def check_password_strength(password):
    strength_from_net = net.evaluate_password_strength(password)  # Appelle la fonction de net.py
    return strength_from_net

# Chiffrement du mot de passe
def encrypt_password(password: str, key: bytes) -> bytes:
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Déchiffrement du mot de passe
def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Stocker les mots de passe dans un fichier JSON
def store_passwords(passwords: dict, filename: str = "passwords.json"):
    with open(filename, 'w') as f:
        json.dump(passwords, f)

# Charger les mots de passe depuis un fichier JSON
def load_passwords(filename: str = "passwords.json") -> dict:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

# Fonction pour enregistrer un mot de passe
def save_password():
    site = search_entry.get()
    password = password_entry.get()
    if site and password:
        encrypted_password = encrypt_password(password, key).decode()
        passwords[site] = encrypted_password
        store_passwords(passwords)
        password_listbox.insert(tk.END, site)
        messagebox.showinfo("Success", f"Password {site} saved.")
    else:
        messagebox.showwarning("Error", "Please enter a site et password.")

# Fonction pour rechercher un mot de passe
def search_password():
    site = search_entry.get()
    if site in passwords:
        encrypted_password = passwords[site]
        password = decrypt_password(encrypted_password.encode(), key)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        messagebox.showinfo("Success", f"Password for {site} found.")
    else:
        messagebox.showwarning("Error", f"No password for {site}.")

# Fonction pour exporter les mots de passe
def export_passwords():
    file_name = simpledialog.askstring("Export", "Name of the file to export :")
    if file_name:
        with open(file_name + '.json', 'w') as f:
            json.dump(passwords, f)
        messagebox.showinfo("Success", "Passwords successfully exported.")

# Fonction pour importer les mots de passe
def import_passwords():
    file_name = simpledialog.askstring("To import", "Name of the file to import :")
    if file_name:
        try:
            with open(file_name + '.json', 'r') as f:
                imported_passwords = json.load(f)
                passwords.update(imported_passwords)
                for site in imported_passwords:
                    password_listbox.insert(tk.END, site)
                messagebox.showinfo("Success", "Passwords sucessfully imported.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during import : {str(e)}")

# Chargement ou génération de la clé de chiffrement
key_filename = "secret.key"
if os.path.exists(key_filename):
    with open(key_filename, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_filename, 'wb') as f:
        f.write(key)

# Charger les mots de passe existants
passwords = load_passwords()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Intelligent password Management and Analysis System")
root.geometry("800x600")

# Chargement de l'image de fond
background_image_path = r"C:\Users\lilyb\3D Objects\background.jpg"
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Création d'un label pour l'image de fond
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Création d'un cadre pour les widgets
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# Champ pour entrer un mot de passe
password_entry = tk.Entry(frame, font=('Courier', 18))
password_entry.place(relwidth=0.65, relheight=1)

# Bouton pour ajouter un mot de passe
add_button = tk.Button(frame, text="Add", font=('Courier', 18), command=save_password)
add_button.place(relx=0.7, relheight=1, relwidth=0.3)

# Indicateur de force du mot de passe
strength_label = tk.Label(root, text="Password strength: ", font=('Courier', 18), bg='#80c1ff')
strength_label.place(relx=0.5, rely=0.2, anchor='n')

# Bouton pour générer un mot de passe
generate_button = tk.Button(root, text="Generate password", font=('Courier', 18), command=generate_password)
generate_button.place(relx=0.5, rely=0.3, anchor='n')

# Liste des mots de passe enregistrés
password_listbox = tk.Listbox(root, font=('Courier', 18))
password_listbox.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.3, anchor='n')

# Champ de recherche de mots de passe
search_entry = tk.Entry(root, font=('Courier', 18))
search_entry.place(relx=0.5, rely=0.85, relwidth=0.65, anchor='n')

# Bouton de recherche de mots de passe
search_button = tk.Button(root, text="Search", font=('Courier', 18), command=search_password)
search_button.place(relx=0.85, rely=0.85, anchor='n')

# Menu de navigation
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="Fichier", menu=file_menu)
file_menu.add_command(label="Export", command=export_passwords)
file_menu.add_command(label="Import", command=import_passwords)
file_menu.add_command(label="Quit", command=root.quit)

# Charger les mots de passe existants dans la liste
for site in passwords:
    password_listbox.insert(tk.END, site)

# Lancer l'application
root.mainloop()