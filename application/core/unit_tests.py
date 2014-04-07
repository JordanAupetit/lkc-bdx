#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

import sys
import lib.utility as utility
import lib.kconfiglib.kconfiglib as kconfiglib
import unittest


"""
==================== IMPORTANT =============================

 test_in  : Represents the function arguments
 test_out : Represents the expected results
 test_res : Represents the result obtained

"""

""" 
    Initialization of options to be tested 
    For instance, you can exec this script like this :
    python unit_tests.py /net/travail/jaupetit/linux-3.13.5
"""

if len(sys.argv) > 0:
    path = sys.argv[1]

    arch = "x86_64"
    srcarch = "x86"
    utility.init_environ(path, arch, srcarch)

    kconfig_infos = kconfiglib.Config(filename=path+"/Kconfig",
        base_dir=path, print_warnings=False)

    top_level_items = kconfig_infos.get_top_level_items()
    menus = kconfig_infos.get_menus()
    top_menus = utility.get_top_menus(menus)
    items = []
    utility.get_all_items(top_level_items, items)

else:
    print "Error -- Please give a kenrle pth in parameter"
    sys.exit("Error -- Please give a kenrle pth in parameter")



class UnitTest(unittest.TestCase):
    """ Class function tests """

    def test_convert_list_xDim_to_1Dim(self):
        """
        This test is testing function convert_list_xDim_to_1Dim 
        whose purpose is to convert a multi-dimensional list 
        a list to a single dimension
        """

        test_in = ["a", "b", "c", "d", "e"]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        self.assertEqual(test_res, test_out)

        test_in = [["a"], ["b"], ["c", "d"], ["e"]]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        self.assertEqual(test_res, test_out)

        test_in = [[[[[[[[["a"]]]]]]]], ["b"], [["c"], ["d"]], [[[["e"]]]]]
        test_out = ["a", "b", "c", "d", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        self.assertEqual(test_res, test_out)

        test_in = [[], ["b"], [["c"]], [[[["e"]]]]]
        test_out = ["b", "c", "e"]
        test_res = utility.convert_list_xDim_to_1Dim(test_in)

        self.assertEqual(test_res, test_out)

    def test_get_symbols_list(self):
        """
        This test is testing function get_symbol_list whose purpose 
        is to convert a tree representing a condition in a list
        giving the names of symbols (options) present in this condition
        """

        sym_a = items[25]
        sym_b = items[26]
        sym_c = items[27]
        sym_d = items[28]
        sym_e = items[29]
        sym_f = items[30]

        # test 1

        test_in = utility.Tree([0, sym_a, sym_b])
        test_out = [sym_a.get_name(), sym_b.get_name()]
        test_res = test_in.get_symbols_list()

        test_out = list(set(test_out))
        test_res = list(set(test_res))

        test_out.sort()
        test_res.sort()

        self.assertEqual(test_res, test_out)

        # test 2

        test_in = utility.Tree([0, [1, sym_a, sym_b], sym_c, sym_d])
        test_out = [sym_a.get_name(), sym_b.get_name(), sym_c.get_name(),
                    sym_d.get_name()]
        test_res = test_in.get_symbols_list()

        test_out = list(set(utility.convert_list_xDim_to_1Dim(test_out)))
        test_res = list(set(utility.convert_list_xDim_to_1Dim(test_res)))

        test_out.sort()
        test_res.sort()

        self.assertEqual(test_res, test_out)

        # test 3

        test_in = utility.Tree([0, [1, sym_a, sym_b], [0, sym_c, sym_e]])
        test_out = [sym_a.get_name(), sym_b.get_name(), sym_c.get_name(),
                    sym_e.get_name()]
        test_res = test_in.get_symbols_list()

        test_out = list(set(utility.convert_list_xDim_to_1Dim(test_out)))
        test_res = list(set(utility.convert_list_xDim_to_1Dim(test_res)))

        test_out.sort()
        test_res.sort()

        self.assertEqual(test_res, test_out)

        # test 4

        test_in = utility.Tree([0, [1, [0, [1, [0, sym_a, sym_b], sym_c], sym_d],
                                    sym_e], sym_f])

        test_out = [sym_a.get_name(), sym_b.get_name(), sym_c.get_name(),
                    sym_e.get_name(), sym_d.get_name(), sym_f.get_name()]
        test_res = test_in.get_symbols_list()

        test_out = list(set(utility.convert_list_xDim_to_1Dim(test_out)))
        test_res = list(set(utility.convert_list_xDim_to_1Dim(test_res)))

        test_out.sort()
        test_res.sort()

        self.assertEqual(test_res, test_out)


    def test_get_first_option_menu(self):
        """
        Returns the index of the first item in a menu 
        Returns -1 => Menu without options
        Returns a number between 0 and the number of options
        """

        for menu_index in menus:
            index = utility.get_first_option_menu(menu_index, items)
            self.assertTrue(index >= -1)
            self.assertTrue(index <= (len(items) - 1))


    def test_get_index_menu_option(self):
        """
        Returns the index of the top menu where there is an option 
        Returns 0 if the option is not in a menu 
        Returns a number between 1 and the number of top menus
        """

        for i in range(len(items) - 1):
            index = utility.get_index_menu_option(i, items, top_menus)
            self.assertTrue(index >= 0)
            self.assertTrue(index <= len(top_menus))


    def test_convert_tuple_to_list(self):
        """ Converts a tuple in a list """

        test_in = ("e1", "e2", "e3", "e4")
        test_out = ["e1", "e2", "e3", "e4"]
        test_res = utility.convert_tuple_to_list(test_in)

        self.assertEqual(test_res, test_out)

        test_in = (1, "e2")
        test_out = [1, "e2"]
        test_res = utility.convert_tuple_to_list(test_in)

        self.assertEqual(test_res, test_out)

        test_in = (("1", "2"), "e2")
        test_out = [["1", "2"], "e2"]
        test_res = utility.convert_tuple_to_list(test_in)

        self.assertEqual(test_res, test_out)

        test_in = (("1", ("1", ((("1", "2"), "2"), "2"))), "e2")
        test_out = [["1", ["1", [[["1", "2"], "2"], "2"]]], "e2"]
        test_res = utility.convert_tuple_to_list(test_in)

        self.assertEqual(test_res, test_out)

        test_in = (("1", ("1", ((()), "2"))), "e2")
        test_out = [["1", ["1", [[], "2"]]], "e2"]
        test_res = utility.convert_tuple_to_list(test_in)

        self.assertEqual(test_res, test_out)


    def test_get_all_items(self):
        """
        Convert a list of Symbols, Choices, Menus, Comments 
        into a list containing only and Symbols 
        Choices. It recovers Symbols on the menus.
        """

        test_out = []
        utility.get_all_items(top_level_items, test_out)

        for item in test_out:
            if item.is_menu():
                raise Exception("There is a menu in the list.")
            elif item.is_comment():
                raise Exception("There is a menu in the list.")


 
if __name__ == "__main__":

    test = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    unittest.TextTestRunner(verbosity=2).run(test)

