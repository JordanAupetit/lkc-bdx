Dossier de test sur les conditions des dépendances et conflits des fichiers KConfig


Récupérer une option : 
-----------------------

opt = c.get_symbols()[?????]

????? => N° de l'option

==============================================================

Récupérer le menu parent d'une option : 
---------------------------------------

menu = opt.get_parent()


==============================================================


Récupérer les référencement (dépendance ?) d'une option :
----------------------------------------

set_de_ref =  opt.get_referenced_symbols()

==============================================================

Récupérer les "select" (set) de l'option (même ceux qui ne répondent pas à la condition)
----------------------------------------------------------------------------------------

set_de_sel = opt.get_selected_symbols()

==============================================================
