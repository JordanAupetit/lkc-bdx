#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    Main

    Ne pas oublier d'inclure le path de kconfiglib dans le PYTHONPATH
    Avant d'executer ce script
    PYTHONPATH=/net/travail/bthiaola/linux-3.13/Kconfiglib
    export PYTHONPATH
"""

import os
import sys

import utility
import kconfiglib


def usage():
    """
       Usage function

       TODO:Il n'y a pas de vérification d'archtecture supportée (pour l'
       instant)
    """

    if len(sys.argv) < 2:
        sys.exit("Require an architecture")


if __name__ == '__main__':
    usage()

    path = "/net/travail/bthiaola/linux-3.13/"
    path_kconfig = path+"Kconfig"

    # Configuration de l'environnement
    # Architecture
    os.environ["ARCH"] = sys.argv[1]
    utility.match(sys.argv[1])

    # Version du noyau
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

    # Instance de la configuration kconfiglib
    c = kconfiglib.Config(filename=path_kconfig,
                          base_dir=path,
                          print_warnings=True)

    print "==== DEBUG ===="
    print ""
    print "Verification de l'architecture"
    print c.get_srcarch()
    print c.get_arch()

    print ""
    print "Vérification du chemin et de la version du noyau"
    print c.get_srctree()
    print os.environ.get("KERNELVERSION")
    print ""
    print "==== FIN DEBUG ===="
    print "==== Si utilisation dans un interpreteur (ipython par exemple) \
l'instance de la configuration kconfiglib est accessible dans \
la variable 'c' ===="

    # On peut ici rajouter nos tests persos.
    # c.get_symbols() ...
    # c.write_config(filename="TOTO")
    #toto = c.get_symbol("CRASH_DUMP").prompts[0][1]
    #titi = utility.Tree(toto)

    #toto = c.get_symbol("X86_UP_APIC").prompts[0][1]
    toto = c.get_symbol("ARCH_SPARSEMEM_ENABLE").def_exprs[0][1]

    #print toto
    titi = utility.convert_tuple_to_list(toto)
    #print titi
    tata = utility.Tree(titi)
    #print tata
    #tptp = utility.SymbolAdvance(c.get_symbol("ARCH_SPARSEMEM_ENABLE"))
    #tptp = utility.SymbolAdvance(c.get_symbol("GENERIC_BUG_RELATIVE_POINTERS"))
    tptp = utility.SymbolAdvance(c.get_symbol("CRASH_DUMP"))
