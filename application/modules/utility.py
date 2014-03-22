#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import re
import sys

load_kconfig = sys.path[0] + "/parser/"
sys.path.append(load_kconfig)
import kconfiglib


def init_environ(path=".", arch="x86_64", srcarch="", srcdefconfig=""):
    """ Initialize environnement """
    # Configuration de l'environnement
    # Architecture
    os.environ["ARCH"] = arch
    os.environ["SRCARCH"] = srcarch
    os.environ["SRCDEFCONFIG"] = srcdefconfig

    # Version du noyau
    if path[len(path) - 1] != "/":
        path += "/"

    f = open(path + "Makefile", "r")

    version = re.search('VERSION = (.*)', f.readline()).group(1)
    patchlevel = re.search("PATCHLEVEL = (.*)", f.readline()).group(1)
    sublevel = re.search("SUBLEVEL = (.*)", f.readline()).group(1)
    extraversion = re.search("EXTRAVERSION = ?(.*)", f.readline()).group(1)

    f.close()

    os.environ["srctree"] = path

    os.environ["VERSION"] = version
    os.environ["PATCHLEVEL"] = patchlevel
    os.environ["SUBLEVEL"] = sublevel
    os.environ["EXTRAVERSION"] = extraversion

    os.environ["KERNELVERSION"] = \
        version + "." + patchlevel + "." + sublevel + extraversion


def get_all_items(items, items_list):
    """ Return all item (symbol | choice | menu)  from items into items_list """
    for item in items:
        if item.is_symbol():
            items_list.append(item)
        elif item.is_menu():
            get_all_items(item.get_items(), items_list)
        elif item.is_choice():
            items_list.append(item)
        elif item.is_comment():
            continue


def get_top_menus(menus):
    top_menus = []
    for menu in menus:
        if menu.get_parent() is None:
            top_menus.append(menu)
    return top_menus


def get_first_option_menu(menu, items):
    current_option_index = -1

    if menu is None:
        current_option_index = 0
    else:
        current_item = menu.get_symbols()[0]
        cpt = 0
        for item in items:
            if(current_item.get_name() == item.get_name()):
                #find = True
                break
            cpt += 1
        current_option_index = cpt

    show = False

    while(show is False):
        current_item = items[current_option_index]
        if current_item.is_symbol():
            if (current_item.get_type() == kconfiglib.BOOL or
                    current_item.get_type() == kconfiglib.TRISTATE):
                show = True
            else:
                current_option_index += 1
        if current_item.is_menu():
            current_option_index += 1
        elif current_item.is_choice():
            current_option_index += 1
        elif current_item.is_comment():
            current_option_index += 1

    return current_option_index


def get_index_menu_option(id_option, options, top_menus):
    if options[id_option].get_parent() is None:
        return 0
    else:
        parent_menu = options[id_option].get_parent()
        while parent_menu.get_parent() is not None:
            parent_menu = parent_menu.get_parent()
        cpt = 1
        for menu in top_menus:
            if menu.get_title() == parent_menu.get_title():
                return cpt
            cpt += 1


def convert_tuple_to_list(tlist):
    """ Convert tlist (list of tuple) into a list of list """
    res = []
    for i in tlist:
        if type(i) is tuple:
            res += [convert_tuple_to_list(list(i))]
        elif type(i) is list:
            for j in i:
                if type(j) is tuple:
                    res += [convert_tuple_to_list(list(j))]
                else:
                    res += [j]
        else:
            res += [i]
    return res


class Tree(object):
    """ Tree class is a tree structure for condition dependencies"""
    def __init__(self, input_cond):
        super(Tree, self).__init__()

        self.val = input_cond[0]
        self.left = input_cond[1]
        if len(input_cond) == 2:
            # Opérateur unaire
            self.right = None
        if len(input_cond) > 3:
            self.right = Tree([self.val] + input_cond[2:])
        if len(input_cond) == 3:
            if type(input_cond[2]) is not list:
                self.right = input_cond[2]
            else:
                self.right = Tree(input_cond[2])
        self.init_op()

    def init_op(self):
        """ Initialize operator string """
        if self.val == 0:
            self.val = "||"
        elif self.val == 1:
            self.val = "&&"
        elif self.val == 2:
            self.val = "!"
        elif self.val == 3:
            self.val = "="

    def get_symbols_list(self):
        """ Return all referenced symbols from tree's condition into a list """
        if self.left is None and self.right is None:
            return self.val
        if self.left is not None and self.right is None:
            return self.left.get_name()
        if self.left is not None \
                and isinstance(self.right, kconfiglib.Symbol):
            return [self.left.get_name(), self.right.get_name()]

        return [self.left.get_name()] + self.right.get_symbols_list()

    def get_cond(self):
        """ Return infix condition in a list """
        pass

    def __str__(self):
        """ Return a fancy description of a tree into string """
        res = ""
        if type(self.left) is list:
            if self.left[0] == 2:
                res += "!" + str(self.left[1].get_name()) + " "
            elif self.left[0] == 3:
                res += str(self.left[1].get_name()) + " = "
                if type(self.left[2]) is str:
                    res += str(self.left[2]) + " "
                else:
                    res += str(self.left[2].get_name())
            res += str(self.val) + " " + str(self.right)
        elif self.left is not None and self.right is None:
            res += str(self.val) + " " + str(self.left.get_name())
        else:
            right_str = ""
            if isinstance(self.right, Tree):
                right_str = str(self.right)
            elif isinstance(self.right, kconfiglib.Symbol) \
                    or isinstance(self.right, kconfiglib.Choice):
                right_str = self.right.get_name()
            res += str(self.left.get_name()) + " " \
                + str(self.val) + " " \
                + right_str
        return res


class SymbolAdvance(object):
    """ Custom symbol class
        Get more information about conditions and dependencies """
    def __init__(self, sym):
        super(SymbolAdvance, self).__init__()
        self.sym = sym
        self.value = self.sym.get_value()

        #Additional dependencies (à revoir)
        if isinstance(self.sym, kconfiglib.Symbol):
            #Revoir, premier item : "y" à enlever
            self.prompts_cond = self.sym.orig_prompts
            self.default_cond = self.sym.def_exprs
            self.selects_cond = self.sym.orig_selects
            self.reverse_cond = self.sym.rev_dep

            self.prompts_tree = None
            self.default_tree = None
            self.selects_tree = None
            self.reverse_tree = None
        elif isinstance(self.sym, kconfiglib.Choice):
            #On verra ca plus tard
            pass
        self.init_trees()

    def init_trees(self):
        """docstring for init_trees"""
        if self.prompts_cond != []:
            self.prompts_tree = Tree(convert_tuple_to_list(
                self.prompts_cond[0][1]))

        if self.default_cond != []:
            self.default_tree = Tree(convert_tuple_to_list(
                self.default_cond[0][1]))

        if self.selects_cond != []:
            self.selects_tree = []
            for cond in self.selects_cond:
                self.selects_tree += [[cond[0],
                                      Tree(convert_tuple_to_list(cond[1]))]]
        if self.reverse_cond != 'n':
            self.reverse_tree = Tree(convert_tuple_to_list(self.reverse_cond))

    def cat_symbols_list(self):
        """ Return all dependencies of a symbol into a list """
        default_symbol = []
        select_symbol_list = []
        prompts_symbol_list = []
        reverse_symbol_list = []

        if self.default_tree is not None:
            default_symbol = self.default_tree.get_symbols_list()

        if self.selects_tree is not None:
            for i in self.selects_tree:
                select_symbol_list += i[1].get_symbols_list()

        if self.prompts_tree is not None:
            prompts_symbol_list = self.prompt_tree.get_symbols_list()

        if self.reverse_tree is not None:
            reverse_symbol_list = self.reverse_tree.get_symbols_list()

        print " === d ===> ", default_symbol
        print " === s ===> ", select_symbol_list
        print " === p ===> ", prompts_symbol_list
        print " === r ===> ", reverse_symbol_list

        final_symbol_list = list(set(default_symbol +
                                     select_symbol_list +
                                     prompts_symbol_list +
                                     reverse_symbol_list))
        return final_symbol_list

    def __str__(self):
        """ Print all conditions in infix form """
        select_str = "None"
        if self.selects_tree is not None:
            select_str = ""
            for cond in self.selects_tree:
                select_str += cond[0].get_name() + " if " + str(cond[1]) + '\n'

        return "Prompts : " + str(self.prompts_tree) + '\n' +\
               "Default : " + str(self.default_tree) + '\n' +\
               "Select : " + select_str + '\n' +\
               "Reverse : " + str(self.reverse_tree)
