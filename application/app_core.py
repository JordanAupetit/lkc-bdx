#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys
import os

sys.path.append("modules/")
import utility
#import search
sys.path.append("parser/")
import kconfiglib


class AppCore(object):
    """ AppCore class """
    def __init__(self):
        super(AppCore, self).__init__()
        self.path = None
        self.arch = None
        self.src_arch = None
        self.config_file = None
        self.arch_defconfig = None
        self.kconfig_infos = None
        self.top_level_items = None
        self.menus = None
        self.sections = None
        self.items = None
        self.cursor = 0
        self.history = []

    def init_memory(self, path, arch, src_arch, config_file=""):
        """ If config_file == "", load default config """
        #if utility.check_config_file(config_file):
        #    pass
        self.path = path
        self.arch = arch
        self.src_arch = src_arch

        if config_file == "":
            self.config_file = config_file
        else:
            self.config_file = self.path + self.src_arch + "/configs/" + self.arch

        utility.init_environ(self.path,
                             self.arch,
                             self.src_arch,
                             self.config_file)

        if path[:-1] != "/":
            path += "/"

        self.kconfig_infos = kconfiglib.Config(filename=path+"Kconfig",
                                               base_dir=path,
                                               print_warnings=False)

        self.top_level_items = self.kconfig_infos.get_top_level_items()
        self.menus = self.kconfig_infos.get_menus()
        self.sections = utility.get_top_menus(self.menus)
        self.items = []
        utility.get_all_items(self.top_level_items, self.items)

    def init_test_environnement(self, path):
        """ Test if the kernel path is correct
        Return a 2D list with all architecture and their defconfig if it is the
        case, else return a error code (-1)
        """
        path_arch = path + "/arch"
        if not os.path.exists(path_arch):
            return -1

        arch_defconfig = []

        list_arch = os.listdir(path_arch)

        #for arch in list_arch:
        #    tmp = path + "/arch/" + arch
        #    if os.path.isdir(tmp):
        #        path_defconfig = tmp + "/configs"
        #        if os.path.exists(path_defconfig):
        #            list_defconfig = os.listdir(path_defconfig)
        #            for defconfig in list_defconfig:
        #                if defconfig[:10] == "_defconfig":
        #                    arch_defconfig += [defconfig[:-10]]
        #                else:
        #                    arch_defconfig += [defconfig]
        #        else:
        #            arch_defconfig += [[arch, arch]]

        #self.arch_defconfig = arch_defconfig
        ##Copy

        for arch in list_arch:
            tmp = path + "/arch/" + arch
            if os.path.isdir(tmp):
                path_defconfig = tmp + "/configs"
                if os.path.exists(path_defconfig):
                    list_defconfig = os.listdir(path_defconfig)
                    arch_defconfig += [[arch, list_defconfig]]

        self.arch_defconfig = arch_defconfig
        return arch_defconfig

    def get_current_opt_name(self):
        """ Return the current option's name """
        return self.items[self.cursor].get_name()

    def get_current_opt_help(self):
        """ Return the current option's help """
        return self.items[self.cursor].get_help()

    def get_current_opt_type(self):
        """ Return the current option's type """
        return self.items[self.cursor].get_type()

    def get_current_opt_vibility(self):
        """ Return the current option's visibility """
        return self.items[self.cursor].get_visibility()

    def get_current_opt_conflict(self):
        """ Return a list of symbols which are in conflict with the current
        option """
        #Revoir si il ne vaudrait pas mieux faire un tableau 2D
        #[symbol, symbolAdvance]
        self.sym_adv = utility.SymbolAdvance(self.items[self.cursor])
        return self.sym_adv.cat_symbols_list()

    def get_current_opt_verbose(self):
        """ Return a option's verbose output """
        return str(self.items[self.cursor])

    def get_all_sections(self):
        """ Return all kernel's sections into a list """
        return self.sections

    def get_result_search(self):
        """docstring for get_result_search"""
        pass

    def goto_opt(self, opt_id):
        """ Goto method, go to the option 'opt_id'
        Increment the history save
        """
        self.history.append(opt_id)
        self.cursor = opt_id

    def goto_back_opt(self):
        """Goto method, go to the previous option on history's save top """
        if len(self.history) > 0:
            self.cursor = self.history.pop()

    def goto_next_opt(self, value_user_cursor):
        """ Goto method, go to the next symbol option
        (not menus/comment/string/hex..) which may be modified or not. """
        #A voir, test pour si valeur par défaut
        if self.cursor < len(self.items):
            self.set_value(value_user_cursor)

            while 1:
                current_item = self.items[self.cursor]

                if current_item.is_symbol():
                    if current_item.get_type() == kconfiglib.BOOL or \
                       current_item.get_type() == kconfiglib.TRISTATE:
                        break
                elif current_item.is_choice():
                    break

                # Menu, comment, unknown, string, hex, int : skip
                self.cursor += 1

            self.history.append(self.cursor)

    def set_current_opt_value(self, value_user_cursor):
        """Set the current option's value with value_user_cursor ("y", "n",
            "m" (if tristate))
        In case of choice, if no choice is selected : value_user_cursor == "N"
        """
        current_item = self.items[self.cursor]

        if current_item.is_symbol():
            self.items[self.current_option_index]\
                .set_user_value(value_user_cursor)
        elif current_item.is_choice():
            items = current_item.get_symbols()
            for i in items:
                if value_user_cursor == "N":
                    # All choices clear
                    i.set_user_value("n")
                elif i.get_name() == value_user_cursor:
                    i.set_user_value("y")
                    break
