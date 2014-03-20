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
            self.right = input_cond[2]
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
            res = str(self.val) + " " + str(self.left.get_name())
        else:
            if isinstance(self.right, Tree):
                right_str = str(self.right)
            elif isinstance(self.right, kconfiglib.Symbol) \
                    or isinstance(self.right, kconfiglib.Choice):
                right_str = self.right.get_name()
            res += str(self.left.get_name()) + " " \
                + str(self.val) + " " \
                + right_str
        return res
