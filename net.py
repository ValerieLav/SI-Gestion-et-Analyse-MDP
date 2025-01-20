import pickle
import numpy as np

# Charger le modèle d'apprentissage automatique
def load_model():
    try:
        with open("password_strength_model.pkl", "rb") as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        raise Exception("Le fichier du modèle 'password_strength_model.pkl' est introuvable. Assurez-vous de l'avoir entraîné et enregistré.")

# Évaluer la force d'un mot de passe
def evaluate_password_strength(password, model):
    features = extract_features(password)
    strength = model.predict(features)
    return strength[0]  # Retourner la première valeur car predict renvoie un tableau

def extract_features(password):
    # Fonction pour extraire les caractéristiques d'un mot de passe
    length = len(password)
    has_upper = int(any(c.isupper() for c in password))
    has_lower = int(any(c.islower() for c in password))
    has_digit = int(any(c.isdigit() for c in password))
    has_special = int(any(c in "!@#$%^&*()" for c in password))

    return np.array([[length, has_upper, has_lower, has_digit, has_special]])

# Main
if __name__ == "_main_":
    model = load_model()  # Charger le modèle une fois pour une utilisation ultérieure

    # Exemple d'utilisation (peut être supprimé dans la version finale)
    password = "Exemple@123"
    strength = evaluate_password_strength(password, model)
    print(f"La force du mot de passe '{password}' est : {strength}")