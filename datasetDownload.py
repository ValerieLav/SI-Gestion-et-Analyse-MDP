import pandas as pd
import numpy as np
import random as rd
import os


# Chargement du dataset
# Attention au chemin de rockyou.txt
pathfile = r'rockyou.txt'

# Garder 10000 lignes aleratoire
n = sum(1 for line in open(pathfile, encoding='latin-1'))  #Nombre de ligne dans le fichier
s = 10000                                                  #Nombre de lignes désirees

skip = sorted(rd.sample(range(n), n-s))
df = pd.read_csv(pathfile,
                 on_bad_lines='skip',
                 encoding="latin-1",
                 skiprows= skip,
                 header=None,
                 names=["password"])                       # Définir le nom de colonne

# Suppresion des doublons
df_clean = df.drop_duplicates()

# Supprimer les espaces en début et fin de chaine
df_clean.loc[:,'password'] = df_clean['password'].str.strip()

# Filtrer les mdp de moins de 6 et au plus de 128 caractere
df_clean = df_clean[df_clean['password'].str.len().between(6,128)]

# Supprimer les mots de passe manquants
df_clean = df_clean.dropna( subset=['password'])

# Filtrer les caracter non autorisés
invalides_chars = df_clean['password'].str.contains(r'[^a-zA-Z0-9!@#$%^&*()]')
df_clean = df_clean[~invalides_chars]

# Supprimer les mots de passe commun
common_pwd = ['123456','password','admin','123456789', '1234567', '12345678']
df_clean = df_clean[~df_clean['password'].isin(common_pwd)]

# Réécrire le DataFrame si certaine ligne sont effacees
df_clean = df_clean.reset_index(drop=True)

# Fonction Calcule de Majuscules
def count_uppercase(pwd) :
    c = 0
    for char in pwd :
        if char.isupper() :
            c += 1
    return c

# Fonction Calcule de Miniscules
def count_lowercase(pwd) :
    c = 0
    for char in pwd :
        if char.islower() :
            c += 1
    return c

# Fonction Calcule de Chiffres
def count_digit(pwd) :
    c = 0
    for char in pwd :
        if char.isdigit() :
            c += 1
    return c

# Fonction calcule de Caractere Speciaux
def count_special_char(pwd) :
    return len(pwd) - ( count_digit(pwd) + 
                       count_lowercase(pwd) + 
                       count_uppercase(pwd) )

# Calcule de la Force d'un mot de passe         # A redefinir ?
def def_strength(pwd, len, upper, lower, digit, spe):
    s = 0
    if len >= 14 :
        s += 2
    elif len >= 8 :
        s += 1
    if digit >= 1 :
        s += 1
    if spe >= 1 :
        s += 1
    if upper >= 1 :
        s += 1
    if RepetitiveCharacteres(pwd) :
        if s != 0 : s -= 1
    return s

def RepetitiveCharacteres(pwd) : 
    repeatCount = 0
    lastCharac = None
    for i in range (1, len(pwd)) :
        lastCharac = pwd[i-1]
        if (pwd[i] == lastCharac) :
            repeatCount += 1
        else :
            repeatCount = 0
        if repeatCount == 2 : return True
    return False

# Fonction extraction des carcateristics
def extract_features(password) : 
    length = len(password)
    upper = count_uppercase(password)
    lower = count_lowercase(password)
    digit = count_digit(password)
    spe = count_special_char(password)
    strength = def_strength(password, length, upper, lower, digit, spe)
    return [password, length, upper, lower, digit, spe, strength]

# Creation du DataFrame avec caracteristics
f = np.array([extract_features(pw) for pw in df_clean['password']])
dff = pd.DataFrame(f, columns=['password', 'length', 'upper', 'lower', 'digit', 'spe', 'strength'])

# Enregistrer dans un fichier df dans dataset
x = rd.randint(1,100)
filename = f'dataset/df{x}.csv'
while os.path.exists(filename):
    x = rd.randint(1,100)
    filename = f'dataset/df{x}.csv'
dff.to_csv(filename)