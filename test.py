import pandas as pd
import numpy as np

#Changement de dataset
df = pd.read_csv(r'/Users/kellyangela/Projet Programmation Python/SI-Gestion-et-Analyse-MDP/rockyou.txt',
                 on_bad_lines='skip',
                 encoding='latin-1',)

#set colums head
df.columns = ["password"]

#Suppresion des doublons
df_clean = df.drop_duplicates()

#Supprimer les espaces en début et fin de chaine
df_clean.loc[:,'password'] = df_clean['password'].str.strip()

#Remplacer les NaN par chaine vide
df_clean.loc[:,'password'] = df_clean['password'].str.replace(r'[^\w\s]', '', regex=True)
#df_clean.loc[:,'password'] = df_clean['password'].fillna('')

#Filtrer les mdp de moins de 6 et au plus de 128 caractere
df_clean = df_clean[df_clean['password'].str.len().between(6,128)]

# Supprimer les mots de passe manquants
df_clean = df_clean.dropna( subset=['password'])

#Filtrer les caracter non autorisés
invalides_chars = df_clean['password'].str.contains(r'[^a-zA-Z0-9!@#$%^&*()]')
df_clean = df_clean[~invalides_chars]

#Supprimer les mots de passe commun
common_pwd = ['123456','password','admin','123456789', '1234567', '12345678']
df_clean = df_clean[~df_clean['password'].isin(common_pwd)]

print(df_clean)

'''
suite 
'''

import pandas as pd
import re
import string


# Definir les caracteristiques d’un mot de passe : longueur, utilisation de majuscules/minuscules,chiffres, caract`eres sp ́eciaux, s ́equence, etc.

# Fonction pour extraire les caractéristiques d'un mot de passe
def extract_spec(password):
    features = {}
    features['length'] = len(password)
    features['has_upper'] = any(c.isupper() for c in password)
    features['has_lower'] = any(c.islower() for c in password)
    features['has_digit'] = any(c.isdigit() for c in password)
    features['has_special'] = any(c in string.punctuation for c in password)
    features['has_sequence'] = bool(re.search(r'(.)\1\1', password))  # Identifie les séquences répétées
    return features

# Appliquer cette fonction à chaque mot de passe de votre DataFrame
df_clean['specificite'] = df_clean['password'].apply(extract_spec)

# Transformer ces caractéristiques en colonnes
df_features = pd.DataFrame(df_clean['specificite'].tolist())
df_final = pd.concat([df_clean, df_features], axis=1)

# Afficher les premières lignes du DataFrame final
print(df_final.head())

# Enregistrer le DataFrame final dans un fichier CSV
#df_final.to_csv('rockyou_spec.csv', index=False)

print("Fichier CSV enregistré avec succès.")




'''
Creation Interface → Enregistrement pwd(interface) in file
    Creation fonction :
        Calcule nombre :
character
upper_chara
lower_chara
digit
special
séquence (à faire)
    Définir les caractéristiques d’une mdp : 
        nb : <6 : faible; <10 : moyen; >10 : fort
        caracter spéciaux: <2 : moyen fort

Creer un new txt avec pwd et caractéristique


'''