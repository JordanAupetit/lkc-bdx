################################################################################
#
# Ce fichier sert à expérimenter la création de tableau de vérité
# avec un nombre de colonne correspondant au nombre d'option.
# Le tableau contient toutes les valeurs possibles pour toutes les options...
#
# TEXTE A LA DEMANDE
#
#################################################################################

import math

def tabCreateLine(nbOpt, i):
    tab = []
    for j in range(nbOpt):
        binValue = ((2**(nbOpt - j)) / 2)
        tab.append(i/binValue % 2)
    return tab
    
nbOption = 3

nbLignes = 2 ** nbOption

print nbLignes

for i in range(nbLignes):
    mytab = tabCreateLine(nbOption, i)
    print mytab 
