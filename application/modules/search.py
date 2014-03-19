import sys
sys.path.append("parser/")

import kconfiglib
import utility
import re


# m a True pour chercher dans les menu, s pour les symboles,
# c pour choix, h pour help

def get_items_for_search(conf, m=False, s=True, c=False, h=False):
    
    items = []
    if c:
        items += conf.get_choices()
    if s:
        items += conf.get_symbols(False)
    if m:
        items += conf.get_menus()
    if h:
        items += conf.get_comments()

    return items

# retourne une liste de tuples (nom, item) d'options qui contiennent
# dans leur nom le patern string
# items contient la liste des options dans laquelle on effectue la recherche

def search_pattern(string, items):

    result = []
    search_string = string.lower()

    for item in items:
        text = ""
        if item.is_symbol() or item.is_choice():
            if item.get_type() in (kconfiglib.BOOL, kconfiglib.TRISTATE,
                                   kconfiglib.STRING):
                text = item.get_name()
        elif item.is_menu():
            text = item.get_title()
        else:
            text = item.get_text()

        if text is not None and search_string in text.lower():
            if item.is_comment():
                item = item.get_parent()
            if item is not None:
                result.append((item.get_name(), item))
        
    return result
    
