#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

from gi.repository import Gtk

import os
import sys
import re

sys.path.append("modules/")
import utility
import search
sys.path.append("parser/")
import kconfiglib

import unittest


class UnitTest(unittest.TestCase):
    def setUp(self):

        path = "/net/travail/jaupetit/linux-3.13.5/"

        arch = "x86_64_defconfig"
        srcarch = "x86"
        srcdefconfig = "x86_64_defconfig"
        utility.init_environ(path, arch, srcarch, srcdefconfig)

        kconfig_infos = kconfiglib.Config(filename=path+"/Kconfig",
            base_dir=path, print_warnings=False)

        self.top_level_items = kconfig_infos.get_top_level_items()
        self.menus = kconfig_infos.get_menus()
        self.top_menus = utility.get_top_menus(self.menus)
        self.items = []
        utility.get_all_items(self.top_level_items, self.items)



    # =====================
    # == Retourne l'indice de la première option dans un menu
    # == Retourne -1 => Menu sans options
    # == Retourne un indice entre 0 et le nombre d'options

    def test_get_first_option_menu(self):
        for m in self.menus:
            index = utility.get_first_option_menu(m, self.items)
            if index < -1 or index > (len(self.items) - 1):
                raise Exception("This function return an \
index out of bounds ## Index value : " + str(index))


    # =====================
    # == Retourne l'indice du top menu où se trouve une option
    # == Retourne 0 si l'option n'est pas dans un menu
    # == Retourne un indice entre 1 et le nombre de top menus

    def test_get_index_menu_option(self):
        for i in range(len(self.items) - 1):
            index = utility.get_index_menu_option(i, self.items, self.top_menus)
            if index < 0 or index > len(self.top_menus):
                raise Exception("This function return an \
index out of bounds ## Index value : " + str(index))




if __name__ == "__main__":

    #unittest.main()
    test = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    unittest.TextTestRunner(verbosity=2).run(test)
    