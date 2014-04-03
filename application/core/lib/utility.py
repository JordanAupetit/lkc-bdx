#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import re

import kconfiglib


def init_environ(path=".", arch="x86_64", srcarch="x86"):
    """ Initialize environnement """
    # Configuration de l'environnement
    # Architecture
    os.environ["ARCH"] = arch.split("_defconfig")[0].split(".config")[0]
    os.environ["SRCARCH"] = srcarch

    print os.environ["ARCH"], os.environ["SRCARCH"]
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


def check_config_file(config_file):
    """ Return True if the config_file is correct
    Else return False
    """
    if not os.path.isfile(config_file):
        return False
    fd = open(config_file, 'r')
    rl = fd.readline()
    correct = True
    while rl != '' and correct is True:
        tmp = rl.rstrip()
        res = re.search("CONFIG_.*", tmp)
        if list(tmp) == [] or tmp[0] == '#' or res is not None:
            rl = fd.readline()
            continue
        correct = False
    return correct


def get_all_items(items, items_list):
    """ Return all item (symbol | choice | menu) from items into items_list """
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


def get_id_option_name(items, name):
    cpt = -1
    for i in items:
        if name == i.get_name():
            break
        cpt += 1
    return cpt


def get_first_option_menu(menu, items):
    current_option_index = -1

    if menu is None:
        current_option_index = 0
    else:
        if menu.get_symbols() != []:
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
        if current_item.is_choice():
            current_option_index += 1
        if current_item.is_comment():
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


def get_symbol_condition(sym):
    """ Return all conditions (verbose) from a symbol into a list :
    [prompt_str, default_str, select_str, reverse_str, additional_str]
    """
    current_item = sym
    current_item_str = str(sym)

    # Zone prompt
    prompt_str = ""
    zonePrompts = str(current_item).split("Prompts:")[1]\
                                   .split(")")[0] + ")"

    if "if " in str(zonePrompts):
        cond_prompt = str(zonePrompts).split("if ")[1]\
                                      .split(")")[0] + ")"
        prompt_str += "condition prompt : " + cond_prompt + "\n"

    # Zone Default
    default_str = ""
    if "Condition:" in current_item_str:
        cond_default = current_item_str.split("Condition:")[1]\
                                       .split(")")[0] + ")"
        default_str += "condition default : " + cond_default + "\n"

    # Zone Select
    select_str = ""
    if "Selects:" in current_item_str:
        zoneSelect = current_item_str.split("Selects:")[1]\
                                     .split("Reverse dependencies:")[0]
        subZone = str(zoneSelect).split("\n")
        for cond in subZone:
            if "if " in str(cond):
                select_str += "condition select : " +\
                              str(cond).split("if ")[1] + "\n"

    # Zone Reverse
    reverse_str = ""
    if "Reverse dependencies:" in current_item_str:
        zoneReverse = current_item_str.split("Reverse dependencies:")[1]\
                                      .split("Additional dependencies")[0]
        subZone = str(zoneReverse).split("\n")
        for cond in subZone:
            if cond != "":
                reverse_str += "condition reverse :" + str(cond) + "\n"

    # Zone Additional
    additional_str = ""
    if "menus and if's:" in current_item_str:
        zoneAdditional = current_item_str.split("menus and if's:")[1]\
                                         .split("Locations:")[0]
        subZone = str(zoneAdditional).split("\n")
        for cond in subZone:
            if cond != "":
                additional_str += "condition additional :" + str(cond) + "\n"

    return [prompt_str, default_str, select_str, reverse_str, additional_str]


def fill_additional_dep(sym, list_conflict=[]):
    """ Fill list_conflict with all symbols referenced
    from additional_cond_str.
    We have do to it manually from __str__ symbol's method because there is no
    symbol attribute for it.
    """
    additional_cond = get_symbol_condition(sym)[4]
    if additional_cond == "":
        return list_conflict
    if "no additional dependencies" not in additional_cond:
        cond = re.sub('condition additional : ', "", additional_cond)
        cond = re.sub('\(value: \"[yn]\"\)', "", cond)
        cond = re.sub('[&&||]', "", cond)
        cond = cond.split(" ")
        for i in cond:
            if i != "":
                list_conflict += [i]
    return list(set(list_conflict))


def print_debug_reverse_dep(sym):
    #curr_sym = self.items[self.cursor]
    #print "----- print_fab_reverse_dep : ", curr_sym.get_name(), " -----"

    #sym_adv = utility.SymbolAdvance(curr_sym)
    #list_tmp = sym_adv.cat_symbols_list()

    #for iTEM in self.items:
    #    if isinstance(iTEM, kconfiglib.Symbol):

    #        sym_adv = utility.SymbolAdvance(iTEM)
    #        list_tmp = sym_adv.cat_symbols_list()
    #        for i in list_tmp:
    #            if i == curr_sym.get_name():
    #                print "-- ", iTEM.get_name(), " --"

    #print list_tmp
    pass


def convert_list_xDim_to_1Dim(llist):
    """ Convert muti-dimensional list into one dimensional list """
    if type(llist) is not list:
        return None
    res = []
    for i in llist:
        if type(i) is list and len(i) > 1:
            res += convert_list_xDim_to_1Dim(i)
        elif i == []:
            continue
        else:
            if type(i) is list:
                res += convert_list_xDim_to_1Dim(i)
            else:
                res += [i]
    return res


def convert_tuple_to_list(tlist):
    """ Convert tlist (list of tuple) into a list of list """
    if tlist is None:
        return None

    if type(tlist) is not list and type(tlist) is not tuple:
        return [tlist]

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
    """ Tree class is a tree structure for condition dependencie s"""
    def __init__(self, input_cond):
        super(Tree, self).__init__()

        if isinstance(input_cond, kconfiglib.Symbol):
            self.val = input_cond
            self.right = None
            self.left = None
            return
        if type(input_cond) is list and len(input_cond) == 1 and\
                isinstance(input_cond[0], kconfiglib.Symbol):
            self.val = input_cond[0]
            self.right = None
            self.left = None
            return

        self.val = input_cond[0]

        if type(input_cond[1]) is not list:
            self.left = input_cond[1]
        else:
            self.left = Tree(input_cond[1])

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

    def get_symbols_list(self):
        """ Return all referenced symbols from tree's condition into a list """
        if self.left is None and self.right is None:
            return self.val
        if self.left is not None and self.right is None:
            if isinstance(self.left, Tree):
                # Not reached
                return self.left.get_symbols_list()
            return self.left.get_name()
        if self.left is not None \
                and isinstance(self.right, kconfiglib.Symbol):
            #print "DEBBUG 12 : ", self.left , " suck " , self.right
            if isinstance(self.left, Tree):
                return [self.left.get_symbols_list(), self.right.get_name()]
            if type(self.left) is not str:
                return [self.left.get_name(), self.right.get_name()]
            return [self.left, self.right.get_name()]

        #print "DEBUG (2) ", self.left

        if type(self.right) is str:
            return [self.left.get_name(), self.right]

        #if type(self.right) is not str:
        if isinstance(self.right, Tree):
            if not isinstance(self.left, Tree):
                if type(self.left) is str:
                    return [self.left, self.right.get_symbols_list()]
                #return [self.left.get_name()] + self.right.get_name()
                return [self.left.get_name(), self.right.get_symbols_list()]
            else:
                return [self.left.get_symbols_list(),
                        self.right.get_symbols_list()]

        if not isinstance(self.left, Tree):
            if type(self.left) is str:
                return [self.left] + self.right.get_name()
            else:
                return [self.left.get_name()] + self.right.get_name()

        return [self.left.get_symbols_list()] + self.right.get_name()

    def get_cond(self):
        """ Return infix condition in a list """
        pass

    def __str__(self):
        """ Return a fancy description of a tree into string ~"""
        res = ""

        if self.left is None and self.right is None:
            return str(self.val)

        if type(self.left) is list:
            res += "!" + str(self.left[1].get_name()) + " " \
                   + str(self.val) + " " + str(self.right)

        elif self.left is not None and self.right is None:
            if not isinstance(self.left, Tree):
                res += str(self.val) + " " + str(self.left.get_name())
            else:
                # Not reached
                res += str(self.val) + " " + str(self.left)
        else:
            right_str = ""
            if isinstance(self.right, Tree):
                right_str = str(self.right)
            elif isinstance(self.right, kconfiglib.Symbol) \
                    or isinstance(self.right, kconfiglib.Choice):
                right_str = self.right.get_name()
            if not isinstance(self.left, Tree):
                res += str(self.left.get_name()) + " " \
                    + str(self.val) + " " \
                    + right_str
            else:
                res += str(self.left) + " " \
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

            self.init_trees()
        else:
            return None

    def init_trees(self):
        """docstring for init_trees"""
        if self.prompts_cond != [] and \
                not isinstance(self.prompts_cond[0][1], kconfiglib.Symbol):
            tmp = convert_tuple_to_list(self.prompts_cond[0][1])
            if tmp is not None:
                self.prompts_tree = Tree(tmp)
        elif self.prompts_cond != [] and \
                isinstance(self.prompts_cond[0][1], kconfiglib.Symbol):
            tmp = self.prompts_cond[0][1]
            if tmp is not None:
                self.prompts_tree = Tree(tmp)

        if self.default_cond != []:
            tmp = None
            if len(self.default_cond[0]) > 1:
                if not isinstance(self.default_cond[0][1], kconfiglib.Symbol):
                    tmp = convert_tuple_to_list(self.default_cond[0][1])
                else:
                    tmp = [self.default_cond[0][1].get_name()]
            else:
                tmp = convert_tuple_to_list(self.default_cond[0])
            if tmp is not None and len(tmp) > 1:
                self.default_tree = Tree(tmp)
            elif tmp is not None and len(tmp) == 1:
                self.default_tree = tmp

        if self.selects_cond != []:
            self.selects_tree = []
            for cond in self.selects_cond:
                if cond[1] is not None and\
                        not isinstance(cond[1], kconfiglib.Symbol):
                    self.selects_tree += \
                        [[cond[0],
                          Tree(convert_tuple_to_list(cond[1]))]]
                elif isinstance(cond[1], kconfiglib.Symbol):
                    self.selects_tree += [[cond[0], Tree(cond[1])]]
        if self.reverse_cond != 'n':
            self.reverse_tree = Tree(convert_tuple_to_list(self.reverse_cond))

    def cat_symbols_list(self):
        """ Return all dependencies of a symbol into a list """
        default_symbol = []
        select_symbol_list = []
        prompts_symbol_list = []
        reverse_symbol_list = []

        if self.default_tree is not None \
                and type(self.default_tree) is not list:
            default_symbol = self.default_tree.get_symbols_list()
        elif self.default_tree is not None \
                and type(self.default_tree) is list:
            default_symbol = self.default_tree

        if self.selects_tree is not None:
            for i in self.selects_tree:
                if len(i) > 1:
                    select_symbol_list += [i[1].get_symbols_list()]

        if self.prompts_tree is not None:
            prompts_symbol_list = self.prompts_tree.get_symbols_list()

        if self.reverse_tree is not None:
            reverse_symbol_list = self.reverse_tree.get_symbols_list()

        aux = [default_symbol,
               select_symbol_list,
               prompts_symbol_list,
               reverse_symbol_list]

        aux = convert_list_xDim_to_1Dim(aux)

        aux2 = []
        for i in aux:
            if isinstance(i, kconfiglib.Symbol):
                aux2 += [i.get_name()]
            else:
                aux2 += [i]

        aux3 = convert_list_xDim_to_1Dim(aux2)
        aux = list(set(aux3))
        return aux

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


class ChoiceAdvance(object):
    """ Custom choice class
        Get more information about conditions and dependencies """
    def __init__(self, list_choice_symbols):
        super(ChoiceAdvance, self).__init__()
        self.list_choice_symbols = list_choice_symbols
        self.syms_advance = []
        for i in list_choice_symbols:
            self.syms_advance += [SymbolAdvance(i)]

    def cat_choice_symbols_list(self):
        """ Return all dependencies of a choice's symbol into a list """
        res = []
        for i in self.syms_advance:
            res += [i.cat_symbols_list()]
        return res
