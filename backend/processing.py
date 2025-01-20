import pandas as pd
import string

# Chargement du dataset
def load_dataset(file_path):
    """
    Charge un dataset à partir d'un fichier CSV.

    Args:
        file_path (str): Le chemin du fichier CSV.

    Returns:
        pd.DataFrame: Un DataFrame contenant les données du fichier CSV.
    """
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', encoding='latin-1', header=None)
        df.columns = ["password"]
        return df
    except Exception as e:
        print(f"Erreur lors du chargement du dataset : {e}")
        return None

# Nettoyage des données
def clean_data(df):
    """
    Nettoie les données en supprimant les doublons et les valeurs manquantes.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.

    Returns:
        pd.DataFrame: Un DataFrame nettoyé.
    """
    return df.drop_duplicates().dropna(subset=['password'])

# Extraire les caractéristiques
def extract_features(pwd):
    """
    Extrait les caractéristiques d'un mot de passe.

    Args:
        pwd (str): Le mot de passe.

    Returns:
        dict: Un dictionnaire contenant les caractéristiques du mot de passe.
    """
    features = {
        'length': len(pwd),
        'num_upper': sum(1 for char in pwd if char.isupper()),
        'num_lower': sum(1 for char in pwd if char.islower()),
        'num_digits': sum(1 for char in pwd if char.isdigit()),
        'num_special': sum(1 for char in pwd if char in string.punctuation),
        'strength': categorize_password(pwd)
    }
    return features

# Catégoriser les mots de passe
def categorize_password(pwd):
    """
    Catégorise un mot de passe en fonction de sa force.

    Args:
        pwd (str): Le mot de passe.

    Returns:
        str: La catégorie du mot de passe ('faible', 'moyen', 'fort', 'invalide').
    """
    if isinstance(pwd, str):
        special_strength = special_char_strength(pwd)
        has_digit = any(char.isdigit() for char in pwd)
        has_upper = any(char.isupper() for char in pwd)

        if len(pwd) < 6:
            return 'faible'
        elif len(pwd) >= 8 and special_strength == 'fort' and has_digit and has_upper:
            return 'fort'
        else:
            return 'moyen'
    else:
        return 'invalide'

def special_char_strength(pwd):
    """
    Détermine la force des caractères spéciaux dans un mot de passe.

    Args:
        pwd (str): Le mot de passe.

    Returns:
        str: La force des caractères spéciaux ('fort', 'moyen', 'faible', 'aucun').
    """
    forts_special_chars = set("!@#$%^&*()")
    moyens_special_chars = set("_-+=[]{}|;:'\",.<>?/")
    faibles_special_chars = set("`~")
    
    if any(char in forts_special_chars for char in pwd):
        return 'fort'
    elif any(char in moyens_special_chars for char in pwd):
        return 'moyen'
    elif any(char in faibles_special_chars for char in pwd):
        return 'faible'
    else:
        return 'aucun'