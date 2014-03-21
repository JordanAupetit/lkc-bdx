#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import re
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
    for item in items:
        if item.is_symbol():
            items_list.append(item)
        elif item.is_menu():
            get_all_items(item.get_items(), items_list)
        elif item.is_choice():
            items_list.append(item)
        elif item.is_comment():
            continue


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
    """docstring for Tree"""
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

    def get_cond(self):
        """ Return infix condition in a list """
        pass

    def __str__(self):
        res = ""
        if type(self.left) is list:
            res += "!" + str(self.left[1].get_name()) + " " \
                   + str(self.val) + " " + str(self.right)
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
    """docstring for SymbolAdvance"""
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
            #On verra ca plutard
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
