# Does a case-insensitive search for a string in the help texts for symbols and
# choices and the titles of menus and comments. Prints the matching items
# together with their locations and the matching text. Used like

import sys
sys.path.append("parser/kconfiglib/")

import kconfiglib
import utility

def search(conf, string, m=True, s=True, c=True):

    result = []

    if string == "":
        return result
    
    search_string = string.lower()

    items = []
    if s:
        items += conf.get_symbols() + conf.get_choices()
    if m:
        items += conf.get_menus()
    if c:
        items += conf.get_comments()
        
    for item in items:
        if item.is_symbol() or item.is_choice():
            text = item.get_help()
        elif item.is_menu():
            text = item.get_title()
        else:
            # Comment
            text = item.get_text()

        # Case-insensitive search
        if text is not None and search_string in text.lower():
            if item.is_comment:
                item = (item.get_parent())
            result.append(item)
            
    return result
