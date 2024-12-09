import tkinter as tk
import random
import string
from tkinter import messagebox

def generate_password(length=12):
    """Génère un mot de passe aléatoire de la longueur spécifiée."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def evaluate_password_strength(password):
    """Évalue la force du mot de passe."""
    if len(password) < 8:
        return "Faible"
    elif (any(char.isdigit() for char in password) and
          any(char.islower() for char in password) and
          any(char.isupper() for char in password) and
          any(char in string.punctuation for char in password)):
        return "Fort"
    else:
        return "Moyen"

def show_generated_password():
    """Affiche le mot de passe généré et évalue sa force."""
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    strength = evaluate_password_strength(password)
    strength_label.config(text=f"Force du mot de passe : {strength}")

def save_password():
    """Enregistre le mot de passe dans un fichier texte."""
    password = password_entry.get()
    if password:
        with open("passwords.txt", "a") as f:
            f.write(password + "\n")
        messagebox.showinfo("Succès", "Mot de passe enregistré avec succès.")
    else:
        messagebox.showwarning("Erreur", "Aucun mot de passe à enregistrer.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Générateur et Évaluateur de Mot de Passe")

# Zone de texte pour entrer un mot de passe
password_entry = tk.Entry(root, width=30)
password_entry.pack(pady=10)

# Label pour afficher la force du mot de passe
strength_label = tk.Label(root, text="")
strength_label.pack(pady=10)

# Bouton pour évaluer la force du mot de passe entré
evaluate_button = tk.Button(root, text="Évaluer la Force", command=lambda: strength_label.config(text=f"Force du mot de passe : {evaluate_password_strength(password_entry.get())}"))
evaluate_button.pack(pady=5)

# Bouton pour générer un mot de passe aléatoire
generate_button = tk.Button(root, text="Générer un Mot de Passe", command=show_generated_password)
generate_button.pack(pady=10)

# Bouton pour enregistrer le mot de passe
button_save = tk.Button(root, text="Enregistrer", command=save_password)
button_save.pack(pady=20)

# Lancement de la boucle principale de l'interface
root.mainloop()