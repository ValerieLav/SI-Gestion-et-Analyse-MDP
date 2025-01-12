import pandas as pd
import numpy as np
import random as rd
import os

# Appel la fonction extraction des carcateristics
from extractFeatures import *

# Chargement du dataset
# Attention au chemin de rockyou.txt
pathfile = r'rockyou.txt'
pathfile_common = r'dataset/10k-most-common.txt'

# Garder 10000 lignes aleratoire
n = sum(1 for line in open(pathfile, encoding='latin-1'))  #Nombre de ligne dans le fichier
s = 10000                                                  #Nombre de lignes désirees

skip = sorted(rd.sample(range(n), n-s))
df = pd.read_csv(pathfile,
                 on_bad_lines='skip',
                 encoding="latin-1",
                 skiprows= skip,
                 header=None,                              # Ignore les noms de colonne du fichier
                 names=["password"])                       # Définir le nom de colonne avec password

# Suppresion des doublons
df_clean = df.drop_duplicates()

# Supprimer les espaces en début et fin de chaine
df_clean.loc[:,'password'] = df_clean['password'].str.strip()

# Filtrer les mdp de moins de 6 et au plus de 28 caractere
df_clean = df_clean[df_clean['password'].str.len().between(6,28)]

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

# Creation du DataFrame avec caracteristics
f = np.array([extract_features(pw) for pw in df_clean['password']])
dff = pd.DataFrame(f, columns=['password', 'length', 'upper', 'lower', 'digit', 'spe', 'strength'])

# Enregistrer dans un fichier df dans dataset
x = rd.randint(1,100)
filename = f'../dataset/df{x}.csv'
while os.path.exists(filename):
    x = rd.randint(1,100)
    filename = f'../dataset/df{x}.csv'
dff.to_csv(filename)