#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import re

# def match(arch):
#     """ Match additional ARCH setting """
#     arch_list = list([["i386", "x86"],
#         ["x86_64", "x86"], ["sparc32", "sparc"],
#         ["sparc64", "sparc"], ["sh64", "sh"],
#         ["tilepro", "tile"], ["tilegx", "tile"]])

#     for arch_iter in arch_list:
#         if arch == arch_iter[0]:
#             os.environ["SRCARCH"] = arch_iter[1]
#             return

#     os.environ["SRCARCH"] = os.environ.get("ARCH")


def init_environ(path=".", arch="x86_64", srcarch="", srcdefconfig=""):
    """ Initialize environnement """
    # Configuration de l'environnement
    # Architecture
    os.environ["ARCH"] = arch
    os.environ["SRCARCH"] = srcarch
    os.environ["SRCDEFCONFIG"] = srcdefconfig
    # match(arch)

    #path_copy = path
    
    # Version du noyau
    if(path[len(path) - 1] != "/"):
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
            continue
        elif item.is_comment():
            continue
