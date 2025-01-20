#####################################################
#                                                   #
#              Importer les Librairies              #
#                                                   #
#####################################################

import pandas as pd
import numpy as np
import random as rd
import os

# Appel la fonction extraction des carcateristics
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractFeatures import *
from gen_mdp import generate_password

#####################################################
#                                                   #
#               Chargement du dataset               #
#                                                   #
#####################################################

pathfile = r'rockyou.txt'

# Garder 10000 lignes aleratoire
n = sum(1 for line in open(pathfile, encoding='latin-1'))  #Nombre de ligne dans le fichier
s = 5000                                                  #Nombre de lignes désirees

skip = sorted(rd.sample(range(n), n-s))
df = pd.read_csv(pathfile,
                 on_bad_lines='skip',
                 encoding="latin-1",
                 skiprows= skip,
                 header=None,                              # Ignore les noms de colonne du fichier
                 names=["password"])                       # Définir le nom de colonne avec password

# Equilibré le dataset avec une génération de mots de passe fort
while (df.size <= 10000) :
    pwd = generate_password(rd.randint(6,20))
    df = df._append({"password": pwd}, ignore_index=True)

#####################################################
#                                                   #
#                Nettoyer le dataset                #
#                                                   #
#####################################################

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

#####################################################
#                                                   #
#              Enregistrer le dataset               #
#                                                   #
#####################################################

x = rd.randint(1,100)
filename = f'df{x}.csv'

# Obtenir le repertoire parent
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Constuire le chemin vers dataset
some_folder_path = os.path.join(parent_dir, 'dataset')
file_to_save = os.path.join(some_folder_path, filename)

while os.path.exists(file_to_save):
    x = rd.randint(1,100)
    filename = f'df{x}.csv'
    file_to_save = os.path.join(some_folder_path, filename)

print(x)
dff.to_csv(file_to_save)
