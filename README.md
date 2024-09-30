# SI-Gestion-et-Analyse-MDP

Password Dataset : https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt?resource=download
A utiliser sur son propre PC, Faire attention au chemin utiliser

import pandas as pd
# Chargement du dataset
df = pd . read_csv (’path/to/rockyou.txt ’)
# Suppression des doublons
df_clean = df . drop_duplicates ()
# Afficher le r s u l t a t
print ( df_clean )
