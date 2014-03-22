#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import kconfiglib


def match(arch):
    """ Match additional ARCH setting """
    arch_list = list([["i386", "x86"],
                      ["x86_64", "x86"], ["sparc32", "sparc"],
                      ["sparc64", "sparc"], ["sh64", "sh"],
                      ["tilepro", "tile"], ["tilegx", "tile"]])

    for arch_iter in arch_list:
        if arch == arch_iter[0]:
            os.environ["SRCARCH"] = arch_iter[1]
            return

    os.environ["SRCARCH"] = os.environ.get("ARCH")


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
        elif self.val == 3:
            self.val = "="

    def get_cond(self):
        """ Return infix condition in a list """
        pass

    def __str__(self):
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
