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
    
# Fonction Verifie si il y a des repetitions de caracteres
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
    
# Calcule de la Force d'un mot de passe         # A redefinir ?
def def_strength(pwd, len, upper, lower, digit, spe):
    s = 0
    if len >= 12 :
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
        
    if s >= 4 :
        return 'fort'
    elif s >= 2: 
        return 'moyen'
    else : 
        return 'faible'

