#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Few utility methods """
import os


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
