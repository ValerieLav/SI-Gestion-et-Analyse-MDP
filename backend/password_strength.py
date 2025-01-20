import random
import string
import spacy

# Charger le modèle de langue anglais de spaCy
nlp = spacy.load('en_core_web_sm')

# Liste de mots communs que l'on souhaite éviter
common_words = ["password", "123456", "qwerty", "admin", "letmein", "welcome"]

# Générateur de mot de passe aléatoire
def generate_password(length=12):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

# Filtrer les mots de passe basés sur des mots communs ou des expressions courantes
def is_password_safe(password):
    for word in common_words:
        if word.lower() in password.lower():
            return False
    doc = nlp(password)
    for token in doc:
        if token.text.lower() in common_words:
            return False
    return True

# Vérifier la robustesse d'un mot de passe
def is_secure_password(password):
    if (any(c.islower() for c in password) and 
        any(c.isupper() for c in password) and 
        any(c.isdigit() for c in password) and 
        any(c in string.punctuation for c in password) and 
        len(password) >= 8):
        return True
    return False