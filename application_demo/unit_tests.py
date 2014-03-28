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


# ==================== IMPORTANT =============================

# test_in : représente les arguements de la fonction
# test_out : représente le résultat attendu
# test_res : représente le résultat obtenu


# ==============
# Fonction de vérification de test

def unit_tests_verify(funcName, tin, tout, tres):

    if tout != tres:
        raise Exception(funcName + " (" + tin + ")" + " [FAILED] ") 


class UnitTest(unittest.TestCase):

    # =====================
    # == Chargement d'une configuration de façon statique
    # == Par la suite, on testera les fonctions avec
    # == différentes architectures

    def load_config(self):
        #path = "/net/travail/jaupetit/linux-3.13.5/"
        path = "/home/jaupetit/linux-3.13.6/"
        #path = "/net/cremi/fberarde/espaces/travail/linux-3.13.3"
        
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
    # == Ce test met à l'épreuve la fonction convert_list_xDim_to_lDim
    # == dont le but est de tranformer une liste à plusieurs dimensions
    # == en une liste à une seule dimension

    def test_convert_list_xDim_to_1Dim(self):

        func_name = "test_convert_list_xDim_to_1Dim"
        
        test_in = ["a", "b", "c", "d", "e"]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        unit_tests_verify(func_name, test_in, test_out, test_res)

        test_in = [["a"], ["b"], ["c", "d"], ["e"]]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        unit_tests_verify(func_name, test_in, test_out, test_res)

        test_in = [[[[[[[[["a"]]]]]]]], ["b"], [["c"], ["d"]], [[[["e"]]]]]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        unit_tests_verify(func_name, test_in, test_out, test_res)

        test_in = [[], ["b"], [["c"]], [[[["e"]]]]]
        test_out = ["b", "c", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        unit_tests_verify(func_name, test_in, test_out, test_res)


    # =====================
    # == Ce test met à l'épreuve la fonction get_symbol_list
    # == dont le but est de transformer un abre représentant une condition
    # == en une liste représentant une condition

    def test_get_symbols_list(self):

        #TODO...
        todo = 1
        
        
    # =====================
    # == Retourne l'indice de la première option dans un menu
    # == Retourne -1 => Menu sans options
    # == Retourne un indice entre 0 et le nombre d'options

    def test_get_first_option_menu(self):
        self.load_config()

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
        self.load_config()

        for i in range(len(self.items) - 1):
            index = utility.get_index_menu_option(i, self.items, self.top_menus)
            if index < 0 or index > len(self.top_menus):
                raise Exception("This function return an \
index out of bounds ## Index value : " + str(index))


    # =====================
    # == Converti un tuple en une liste

    def test_convert_tuple_to_list(self):

        test_in = ("element1", "element2", "element3", "element4")
        test_out = utility.convert_tuple_to_list(test_in)

        if type(test_out) is not list:
            raise Exception("This function don't return a list")

        test_in = (1, "element2")
        test_out = utility.convert_tuple_to_list(test_in)

        if type(test_out) is not list:
            raise Exception("This function don't return a list")

        test_in = (("1", "2"), "element2")
        test_out = utility.convert_tuple_to_list(test_in)

        if type(test_out) is not list:
            raise Exception("This function don't return a list")

        test_in = (("1", ("1", ((("1", "2"), "2"), "2"))), "element2")
        test_out = utility.convert_tuple_to_list(test_in)

        if type(test_out) is not list:
            raise Exception("This function don't return a list")

        test_in = (("1", ("1", ((()), "2"))), "element2")
        test_out = utility.convert_tuple_to_list(test_in)

        if type(test_out) is not list:
            raise Exception("This function don't return a list")


    # =========================
    # == Converti une liste de Symbols, Choices, Menus, Comments
    # == en une liste contenant uniquement des Symbols et des 
    # == Choices. Elle récupère les Symbols dans les menus.

    def test_get_all_items(self):
        self.load_config()
        test_out = []
        utility.get_all_items(self.top_level_items, test_out)

        for item in test_out:
            if item.is_menu():
                raise Exception("There is a menu in the list.")
            elif item.is_comment():
                raise Exception("There is a menu in the list.")



if __name__ == "__main__":

    test = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    unittest.TextTestRunner(verbosity=2).run(test)
    