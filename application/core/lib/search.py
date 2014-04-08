#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Search module """

import kconfiglib.kconfiglib as kconfiglib


def get_items_for_search(conf,
                         menu=False,
                         symbol=True,
                         choice=True,
                         description=False):
    """ m must be True to search into menus, s for symbols, c for choices
        and description for the prompt (kconfiglib) """
    items = []

    if description and not menu and not symbol and not choice:
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
    """ return a list of tuples (name, item) of options which contain in their 
    name the patern 'string'.
    items is the list of options in which the search is performed. """
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
