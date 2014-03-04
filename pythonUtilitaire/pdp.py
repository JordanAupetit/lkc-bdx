#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Few utility methods """
import os
import sys


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


def usage():
    """
       Usage function

       TODO:Il n'y a pas de verification d'archtecture supportee (pour l'
       instant)
    """

    if len(sys.argv) < 2:
        sys.exit("Require an architecture")


def main():
    """ Main function """
    usage()

    os.environ["ARCH"] = sys.argv[1]
    match(sys.argv[1])

    return

if __name__ == '__main__':
    """
        Ne pas oublier d'inclure le path de kconfiglib dans le PYTHONPATH
        Avant d'executer ce script
        PYTHONPATH=/net/travail/bthiaola/linux-3.13/Kconfiglib
        export PYTHONPATH
    """

    main()
    import kconfiglib

    path = "/net/travail/bthiaola/linux-3.13/"
    path_kconfig = path+"Kconfig"

    version = "3"
    patchlevel = "13"
    sublevel = "0"
    extraversion = ""

    os.environ["srctree"] = path

    os.environ["VERSION"] = version
    os.environ["PATCHLEVEL"] = patchlevel
    os.environ["SUBLEVEL"] = sublevel
    os.environ["EXTRAVERSION"] = extraversion

    os.environ["KERNELVERSION"] = version + "." + patchlevel + "." + sublevel

    c = kconfiglib.Config(filename=path_kconfig, base_dir=path,
            print_warnings=True)

    print "==== DEBUG ===="
    print ""
    print "Verification de l'architecture"
    print c.get_srcarch()
    print c.get_arch()

    print ""
    print "Verification du chemin et de la version du noyau"
    print c.get_srctree()
    print os.environ.get("KERNELVERSION")
    print ""
    print "==== FIN DEBUG ===="
    print "==== Si utilisation dans un interpreteur (ipython par exemple) \
l'instance de la configuration kconfiglib est accessible dans \
la variable 'c' ===="

    # On peut ici rajouter nos tests persos.
    # c.get_symbols() ...
