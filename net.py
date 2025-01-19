import pandas as pd
import numpy as np
import random as rd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

from extractFeatures import *

file_path = r'dataset/df18.csv'

df = pd.read_csv(file_path,
                  on_bad_lines='skip',
                  encoding="latin-1")

# Convertir les labels en valeurs numériques
label_mapping = {'faible': 0, 'moyen': 1, 'fort': 2}
df['strength'] = df['strength'].map(label_mapping)

# Separer Caracteristique et Labels
X = df[['length', 'upper', 'lower', 'digit', 'spe']]
y = df['strength']

# Diviser les donnees entrainement et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1000)

# Normaliser les données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialiser et entrainer le modele knn
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train_scaled, y_train)

# Prediction et Evaluation du modele
y_pred = knn.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy}')
# print(classification_report(y_test, y_pred))

def test_input(ipt):
    user_inp = ipt
    user_inp_f = np.array(extract_features(user_inp)).reshape(1, -1)
    #print(user_inp_f)
    df_inp = pd.DataFrame(user_inp_f, columns=['password', 'length', 'upper', 'lower', 'digit', 'spe', 'strength'])
    inp_x = df_inp[['length', 'upper', 'lower', 'digit', 'spe']].values
    inp_y = df_inp['strength']
    inp_pred = scaler.transform(inp_x)

    #print(df_inp)

    strength = knn.predict(inp_pred)

    if strength == 2 : 
        return 'Fort'
    elif strength == 1 : 
        return 'Moyen'
    else : 
        return 'Faible'