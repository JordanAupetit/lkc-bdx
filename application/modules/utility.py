#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import re

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


def init(path=".", arch="x86_64"):
    """ Initialize environnement """
    # Configuration de l'environnement
    # Architecture
    os.environ["ARCH"] = arch
    match(arch)

    path_copy = path
    
    # Version du noyau
    if(path_copy[len(path) - 1] != "/"):
        path_copy += "/"

    f = open(path_copy + "Makefile", "r")
    
    version = re.search('VERSION = (.*)', f.readline()).group(1)
    patchlevel = re.search("PATCHLEVEL = (.*)", f.readline()).group(1)
    sublevel = re.search("SUBLEVEL = (.*)", f.readline()).group(1)
    extraversion = re.search("EXTRAVERSION = ?(.*)", f.readline()).group(1)

    f.close()

    os.environ["srctree"] = path_copy

    os.environ["VERSION"] = version
    os.environ["PATCHLEVEL"] = patchlevel
    os.environ["SUBLEVEL"] = sublevel
    os.environ["EXTRAVERSION"] = extraversion

    os.environ["KERNELVERSION"] = \
        version + "." + patchlevel + "." + sublevel + extraversion
