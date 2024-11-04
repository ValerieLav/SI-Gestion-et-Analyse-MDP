import tkinter as tk
import re

# Fonction pour vérifier les conditions de sécurité du mot de passe
def check_password_strength(password):
    conditions = {
        "8 caractères minimum": len(password) >= 8,
        "Au moins une majuscule": re.search(r"[A-Z]", password) is not None,
        "Au moins un chiffre": re.search(r"[0-9]", password) is not None,
        "Au moins un caractère spécial": re.search(r"[!@#$%^&*()_+-=]", password) is not None
    }

    # Mise à jour des labels en fonction des conditions
    for condition, label in conditions_labels.items():
        label.config(fg="green" if conditions[condition] else "red")

# Fonction de gestion de l'entrée de mot de passe
def on_password_entry(event):
    password = password_entry.get()
    check_password_strength(password)

# Création de la fenêtre principale
window = tk.Tk()
window.title("Conditions pour un mot de passe fort")

# Champ pour saisir le mot de passe
tk.Label(window, text="Entrez votre mot de passe :").pack(pady=5)
password_entry = tk.Entry(window, show="*")
password_entry.pack(pady=5)
password_entry.bind("<KeyRelease>", on_password_entry)

# Labels pour chaque condition
conditions_labels = {}
conditions_texts = ["8 caractères minimum", "Au moins une majuscule", "Au moins un chiffre", "Au moins un caractère spécial"]
for text in conditions_texts:
    label = tk.Label(window, text=text, fg="red")
    label.pack(anchor="w")
    conditions_labels[text] = label

# Lancement de l'interface
window.mainloop()
