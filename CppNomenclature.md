Ce document est une ébauche

Voici le site qui nous serivira de base pour la convention de nommage de nos entités en C++.

http://users.ece.cmu.edu/~eno/coding/CCodingStandard.html

Description sommaire en français :

# Normes à respecter pour coder en C++
======================================

## Les variables
----------------

* Les variables commencent par une minuscule.
* Les variables ne doivent comporter que des caractères de l'alphabet ou des chiffres.

Exemple : int parserId;

## Les fonctions
----------------

* Les fonctions commencent par une minuscule.
* Les fonctions doivent être sous la forme A_B().
  * A représente le groupe de la fonction.
  * B représente le nom de la fonction.

Exemple : parser_read(const char*);

## Les structures
-----------------

* Les structure commencent par une minuscule.
* Le nom des structures doit se terminer par '_t'

Exemple : struct parser_t;

## Objets
---------

* Les classes sont à utiliser au minimum. Il en va de même pour l'héritage (qui est disponible sur les structures en plus des classes).

## Indentation
--------------

* On utilise des "Espaces" et non des "Tabulations".
* L'indentation sera de taille 4.

## Define
---------

* Les variables pré-processeur define doivent être en majuscule, séparées par des underscores.

Exemple : #define MAX_CHAR 255;

Note : Il en va de même pour les variables global const.

## Valeur bool
--------------

J'accepte le type "bool" (valeur true/false) pour les comparaisons et retours de fonctions, bien qu'il fasse parti des librairies C++.

## Enumération
---------------

* Le nom des énumérations doit se terminer par '_t'
* Les valeurs des énumérations doivent être en majuscule.

Exemple : typedef enum {RANDOM, IMMEDIATE, SEARCH} strategy_t;

## Taile des lignes
-------------------

* Une ligne ne doit pas dépasser 80 caractères.

## Utilisation des espaces
--------------------------

* Les espaces seront utilisés comme ci-dessous :

<pre>
if (condition) {
}

while (condition) {
}

strcpy(s, s1);

return 1;
</pre>






