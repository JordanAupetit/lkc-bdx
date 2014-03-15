import sys
sys.path.append("parser/kconfiglib/")

import kconfiglib
import utility
import re

# retourne une liste de tuples (nom, item) d'options qui contiennent
# dans leur nom le patern string
# m a True pour chercher dans les menu, s pour les symboles,
# c pour choix, h pour help
# la liste de tuples est triée sur le nom de l'option
def search(conf, string, m=False, s=True, c=False, h=False):

    result = []

    if string == "":
        return result
    
    search_string = string.lower()

    items = []
    if c:
        items += conf.get_choices()
    if s:
        items += conf.get_symbols() 
    if m:
        items += conf.get_menus()
    if h:
        items += conf.get_comments()

    for item in items:
        text = ""
        if item.is_symbol() or item.is_choice():
            if item.get_type() in (kconfiglib.BOOL, kconfiglib.TRISTATE,
                                   kconfiglib.STRING):
                text = item.get_name()
        elif item.is_menu():
            text = item.get_title()
        else:
            # Comment
            text = item.get_text()

        # Case-insensitive search
        if text is not None and search_string in text.lower():
            if item.is_comment():
                item = item.get_parent()
            if item is not None:
                result.append((item.get_name(), item))
        
    return sorted(result)
    
