#####################################################
#                                                   #
#              Importer les Librairies              #
#                                                   #
#####################################################

import pandas as pd
import numpy as np
import random as rd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

import sys
sys.path.append('../')

from extractFeatures import *

#####################################################
#                                                   #
#               Chargement du dataset               #
#                                                   #
#####################################################

file_path = r'../dataset/df52.csv'

df = pd.read_csv(file_path,
                  on_bad_lines='skip',
                  encoding="latin-1")

#####################################################
#                                                   #
#           Application Modele Supervise            #
#                                                   #
#####################################################

# Split into features and labels
X = df[['length', 'upper', 'lower', 'digit', 'spe']]
y = df['strength']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1000)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the KNN model
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train_scaled, y_train)

# Make predictions and evaluate the model
y_pred = knn.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))