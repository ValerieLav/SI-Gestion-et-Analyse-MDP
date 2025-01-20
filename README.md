# SI-Gestion-et-Analyse-MDP

### Objectifs du projet

1. Analyse la force des mots de passe fournis par les utilisateurs
2. Générer des mots de passe robustes adaptes au besoin des utilisateurs
3. Stocker les mots de passe de maniere sécurisee a l'aide de chiffrement
4. Simuler des attaques de brute-force et de dictionnaire pour tester la robustesse des mots de passe
5. Appliquer des tecchnique de traitement de langage naturel pour eviter les mots de passe bases sur les expression ou mots courrants.

### Password Dataset : [rockyou.txt](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt?resource=download)

### Lien GitHub : https://github.com/ValerieLav/SI-Gestion-et-Analyse-MDP.git

---
## Caractéristiques

- Structure Basique
- Ecrit en Python

## Commancer

### Prérequis
- Python et ses librairies

### Exécuter le Projet
- `python3 init.py`

## Structure

- `init.py` : Fenêtre Principale du Projet
- `net.ipynb` : Machine Learning
- setData File : Fichier pour intialiser la base de Donnée pour le Machine Learning
- dataset : Les databases utilisable ou de test
- `CountFunc.py` et `extractFeatures.py`: Fonction pour effectuer le Machine Learning
- `gen_mdp.py` : Fonction de génération de mot de passe
- `attaque.py` : Fonction simulation d'attaque

## Ce qui est à prévoir ou améliorable

- Formulaire :
    - La base de donnée appartient et est gérer par l'utilisateur
    - Evaluation des mots de passe en se passant sur d'autre caractéristique tel que : nom, prénom, date d'anniversaire, mail, nom du site, ...

## Contributions
- Leila Njoya
- Darren Tchagwo
- Valérie Lav
- Kelly Vaniarison
- Romain Voltigeur