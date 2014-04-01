#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Search module """

import sys
sys.path.append("parser/")
import kconfiglib


def get_items_for_search(conf,
                         menu=False,
                         symbol=True,
                         choice=True,
                         description=False):
    """ m a True pour chercher dans les menu, s pour les symboles, c pour
    choix, h pour help """    
    items = []

    if description and not menu and not symbol and not choice and not help_h:
        items += conf.get_choices()
        items += conf.get_symbols(False)
        return items
    
    if choice:
        items += conf.get_choices()
    if symbol:
        items += conf.get_symbols(False)
    if menu:
        items += conf.get_menus()


def search_pattern(string,
                   items,
                   name=True,
                   description=False,
                   help_h=False):
    
    """ retourne une liste de tuples (nom, item) d'options qui contiennent dans
    leur nom le patern string items contient la liste des options dans laquelle
    on effectue la recherche """
    
    result = []
    search_string = string.lower()

    for item in items:
        text = ""
        if item.is_symbol() or item.is_choice():            
            if item.get_type() in (kconfiglib.BOOL, kconfiglib.TRISTATE):
                if name:
                    get_name = item.get_name()
                    if get_name is None:
                        continue
                    text += get_name
                
                if description:
                    d = item.get_prompts()
                    if d:
                        for i in d:
                            if i is not None:
                                text += ":" + i
                if help_h:
                    h = item.get_help()
                    if h:
                        text += ":" + h
                        
        elif item.is_menu():
            text += item.get_title()
            
        elif item.is_comment():
            None

        if description:
            d = item.get_prompts()
            if d:
                for i in d:
                    if i is not None:
                        text += ":" + i

        if text is not None and search_string in text.lower():
            if item is not None:
                result.append((item.get_name(), item))
    return result
