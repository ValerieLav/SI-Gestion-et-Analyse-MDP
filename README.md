# SI-Gestion-et-Analyse-MDP
---
### Objectifs du projet

1. Analyse la force des mots de passe fournis par les utilisateurs
2. Générer des mots de passe robustes adaptes au besoin des utilisateurs
3. Stocker les mots de passe de maniere sécurisee a l'aide de chiffrement
4. Simuler des attaques de brute-force et de dictionnaire pour tester la robustesse des mots de passe
5. Appliquer des tecchnique de traitement de langage naturel pour eviter les mots de passe bases sur les expression ou mots courrants.
---

Password Dataset : [rockyou.txt](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt?resource=download)

Faire attention au chemin utiliser pour le fichier rockyou.txt

```
import pandas as pd

# Chargement du dataset
df = pd . read_csv (’path/to/rockyou.txt ’)

# Suppression des doublons
df_clean = df . drop_duplicates ()

# Afficher le resultat
print ( df_clean )
```
---

##### Update your branch
Dans le terminal terminal

```
git checkout custom_branch && git rebase main
```
