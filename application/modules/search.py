#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Search module """

import sys
sys.path.append("parser/")
import kconfiglib


def get_items_for_search(conf,
                         menu=False,
                         symbol=True,
                         choice=False,
                         help_h=False,
                         description=False):
    """ m a True pour chercher dans les menu, s pour les symboles, c pour
    choix, h pour help """

    items = []
    if choice:
        items += conf.get_choices()
    if symbol:
        items += conf.get_symbols(False)
    if menu:
        items += conf.get_menus()
    if help_h:
        items += conf.get_comments()
    return items


def search_pattern(string, items):
    """ retourne une liste de tuples (nom, item) d'options qui contiennent dans
    leur nom le patern string items contient la liste des options dans laquelle
    on effectue la recherche """

    result = []
    search_string = string.lower()

    for item in items:
        text = ""
        if item.is_symbol() or item.is_choice():
            if item.get_type() in (kconfiglib.BOOL, kconfiglib.TRISTATE):
                                   #kconfiglib.STRING):
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
