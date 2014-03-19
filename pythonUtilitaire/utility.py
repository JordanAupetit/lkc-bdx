#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os


class Tools(object):
    """docstring for Tools"""

    def match(self, arch):
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

    def convert_tuple_to_list(self, tlist):
        res = []
        for i in tlist:
            if type(i) is tuple:
                res += [self.convert_tuple_to_list(list(i))]
            elif type(i) is list:
                for i2 in i:
                    if type(i2) is tuple:
                        res += [self.convert_tuple_to_list(list(i2))]
                    else:
                        res += [i2]
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
        if self.val == 0:
            self.val = "||"
        elif self.val == 1:
            self.val = "&&"
        elif self.val == 2:
            self.val = "!"

    def __str__(self):
        res = ""
        if type(self.left) is list:
            res += "!" + str(self.left[1].get_name()) + " "\
                   + str(self.val) + " " + str(self.right)

        elif self.left is not None and self.right is None:
            res = str(self.val) + " " + str(self.left.get_name())
        else:
            if isinstance(self.right, Tree):
                right_str = str(self.right)
            else:
                right_str = self.right.get_name()
            res += str(self.left.get_name()) + " " \
                + str(self.val) + " " \
                + right_str

        return res
