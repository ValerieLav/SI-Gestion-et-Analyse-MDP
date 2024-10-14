import pandas as pd
import numpy as np

#Changement de dataset
df = pd.read_csv(r'C:/Users/roroxi/Downloads/rockyou.txt',
                 on_bad_lines='skip',
                 encoding='latin-1',)

#set colums head
df.columns = ["password"]

#Suppresion des doublons
df_clean = df.drop_duplicates()

#Afficher résultat
print(df_clean)