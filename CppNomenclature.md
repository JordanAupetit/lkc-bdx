Ce document est une ébauche


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







