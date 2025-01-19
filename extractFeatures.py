# Appel des fonctions de calcule
from CountFunc import *

# Fonction extraction des carcateristics
def extract_features(password) : 
    length = len(password)
    upper = count_uppercase(password)
    lower = count_lowercase(password)
    digit = count_digit(password)
    spe = count_special_char(password)
    strength = def_strength(password, length, upper, lower, digit, spe)
    return [password, length, upper, lower, digit, spe, strength]
