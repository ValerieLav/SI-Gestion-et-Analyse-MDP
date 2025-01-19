import random

# TEST Utilisation fonction de la bibliothèque random
try:
    test_value = random.randint(1, 10)  # Génère un nombre entre 1 et 10
    print("Bibliothèque random importée avec succès.")
    print("Valeur test générée :", test_value)
except NameError as e:
    print("Erreur : random n'a pas été importée correctement.")

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special_chars = "!@#$%^&*()-_=+"

def contains_common_patterns(password):
    # Liste de motifs communs à éviter dans les mots de passe
    common_patterns = ["1234", "abcd", "qwerty", "1111", "aaaa"]

    # Vérifier chaque motif dans la liste
    for pattern in common_patterns:
        if pattern in password:
            return True  # Retourne True si un motif commun est trouvé

    return False  # Retourne False si aucun motif commun n'est trouvé

def generate_password(length):

    # Sélectionner un caractère de chaque ensemble pour garantir la diversité
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Compléter le reste du mot de passe en sélectionnant aléatoirement parmi tous les ensembles
    all_chars = lowercase + uppercase + digits + special_chars
    password += random.choices(all_chars, k=length - 4)

    # Mélanger les caractères pour éviter que l'ordre ne soit prévisible
    random.shuffle(password)

    # Convertir la liste en chaîne de caractères et la retourner
    return ''.join(password)

# Générer un mot de passe entre 6 et 20 caractères
length = random.randint(6,20)
password = generate_password(length)
if password:
    print("Mot de passe généré :", password)
