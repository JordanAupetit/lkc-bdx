#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" AppCore """


import sys
import os
import re

sys.path.append("modules/")
import utility
import search
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
        self.top_menus = None
        self.sections = None
        self.items = None
        self.cursor = -1
        self.history = []

    def init_memory(self, path, arch, src_arch, config_file="", callback=None):
        """ If config_file == "", load default config """
        if config_file != "":
            if not self.is_config_file_correct(config_file):
                return -1
        self.path = path
        self.arch = arch
        self.src_arch = src_arch

        self.config_file = config_file
        if config_file == "":
            self.config_file = self.path + "arch/" + self.src_arch

            if self.config_file[:-1] != "/":
                self.config_file += "/"

            for i in self.arch_defconfig:
                if src_arch == i[0]:
                    if type(i[1]) is list:
                        self.config_file += "configs/" + self.arch
                        break
                    else:
                        self.config_file += "defconfig"
                        break

        utility.init_environ(self.path,
                             self.arch,
                             self.src_arch)

        if path[-1] != "/":
            path += "/"

        self.kconfig_infos = kconfiglib.Config(filename=path+"Kconfig",
                                               base_dir=path,
                                               print_warnings=False,
                                               callback=callback)

        ret = self.kconfig_infos.load_config(self.config_file)

        if ret != -1:
            self.top_level_items = self.kconfig_infos.get_top_level_items()
            self.menus = self.kconfig_infos.get_menus()
            self.top_menus = utility.get_top_menus(self.menus)
            self.sections = utility.get_top_menus(self.menus)
            self.items = []
            utility.get_all_items(self.top_level_items, self.items)
        else:
            return -1

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

        for arch in list_arch:
            tmp = path + "/arch/" + arch
            if os.path.isdir(tmp):
                path_defconfig = tmp + "/configs"
                if os.path.exists(path_defconfig):
                    list_defconfig = os.listdir(path_defconfig)
                    arch_defconfig += [[arch, list_defconfig]]
                elif os.path.isfile(tmp + "/defconfig"):
                    arch_defconfig += [[arch, "defconfig"]]

        self.arch_defconfig = arch_defconfig
        return arch_defconfig

    def is_config_file_correct(self, config_file):
        """ Return True if the config_file is correct or not """
        return utility.check_config_file(config_file)

    def get_srcarch(self):
        """ Return the current srcarch """
        return self.kconfig_infos.get_srcarch()

    def get_number_options(self):
        """ Return the number of options """
        return len(self.items)

    def get_all_defconfig(self):
        """ Return all arch available into a 2D list"""
        return self.arch_defconfig

    def get_all_topmenus_name(self):
        """ Return all menus name into a list """
        res = [m.get_title() for m in self.top_menus]
        return res

    def get_current_opt_name(self):
        """ Return the current option's name """
        return self.items[self.cursor].get_name()

    def get_current_opt_value(self):
        """ Return the current option's value """
        return self.items[self.cursor].get_value()

    def get_current_opt_prompt(self):
        """ Return the current option's prompt """
        return self.items[self.cursor].get_prompts()

    def get_current_opt_help(self):
        """ Return the current option's help """
        help_text = self.items[self.cursor].get_help()
        if help_text is None:
            help_text = "No help available."
        return help_text

    def get_current_opt_type(self):
        """ Return the current option's type """
        return self.items[self.cursor].get_type()

    def get_current_choice_symbols_name(self):
        """ Return all current choice's symbols and their value into a list
        [[name, value], [name, value] ..]
        If current item is not a choice, return None
        """
        if self.is_current_opt_choice():
            res = []
            for i in self.items[self.cursor].get_symbols():
                res += [[i.get_name(), i.get_value()]]
            return res
        return None

    def is_current_opt_bool(self):
        """ Return True if current option is bool """
        return self.items[self.cursor].get_type() == kconfiglib.BOOL

    def is_current_opt_tristate(self):
        """ Return True if current option is bool """
        return self.items[self.cursor].get_type() == kconfiglib.TRISTATE

    def is_current_opt_symbol(self):
        """ Return True if current option is a symbol """
        return self.items[self.cursor].is_symbol()

    def is_current_opt_choice(self):
        """ Return True if current option is a choice """
        return self.items[self.cursor].is_choice()

    def is_selection_opt_choice_possible(self, choice_selection):
        """ Return True if choice_selection is modifiable """
        if self.is_current_opt_choice():
            if self.get_current_opt_visibility() == "n":
                if self.items[self.cursor].get_selection() is None:
                    return False
                else:
                    for name, value in self.get_current_choice_symbols_name():
                        if value == "y" and name != choice_selection:
                            return False
                return True
        # Not a choice
        return None

    def is_current_opt_modifiable(self):
        """ Return True if current option is modifiable """
        return self.items[self.cursor].is_modifiable()

    def has_option_selected(self):
        """ Return True if no option is selected """
        return self.cursor >= 0

    def get_current_opt_index(self):
        """ Return the current option's index """
        return self.cursor

    def get_current_opt_visibility(self):
        """ Return the current option's visibility """
        return self.items[self.cursor].get_visibility()

    def get_current_opt_parent_topmenu(self):
        """ Return the current option's first menu position """
        return utility.get_index_menu_option(self.cursor,
                                             self.items,
                                             self.top_menus)

    def get_first_option_menu(self):
        """ Return the first option menu """
        return utility.get_first_option_menu(None, self.items)

    def get_id_option_menu(self, id_menu):
        """ Return the 'id' option by menu """
        return utility.get_first_option_menu(self.top_menus[id_menu], self.items)

    def get_id_option_name(self, name):
        """ Return the 'id' option by name
        -1 if name doesn't exist
        """
        return utility.get_id_option_name(self.items, name)

    def get_current_opt_parent_topmenu_str(self):
        """ Return the current option's first menu position """
        if self.items[self.cursor].get_parent() is None:
            return "Current menu: General options"
        else:
            return "Current menu: " + self.items[self.cursor].get_parent()\
                                                             .get_title()

    def get_current_opt_conflict(self):
        """ Return a list of symbols which are in conflict with the current
        option.
        If current option is a choice, return a multi-dimensional list
        of all choice's symbols'
        """
        list_res = []
        if self.is_current_opt_symbol():
            curr_sym = self.items[self.cursor]
            sym_adv = utility.SymbolAdvance(curr_sym)
            list_tmp = sym_adv.cat_symbols_list()
            list_res = [curr_sym.get_name(),
                        self._fill_conflict_process(list_tmp)]
        elif self.is_current_opt_choice():
            for sym in self.items[self.cursor].get_items():
                tmp = utility.SymbolAdvance(sym)
                list_tmp = tmp.cat_symbols_list()
                list_res += [[sym.get_name(),
                             self._fill_conflict_process(list_tmp)]]
        return list_res

    def _fill_conflict_process(self, list_conflict):
        """docstring for _fill_conflict_process"""
        list_res = []
        for conflict in list_conflict:
            c = self.kconfig_infos.get_symbol(conflict)
            if c is not None:
                if c.get_type() == kconfiglib.BOOL\
                        or c.get_type() == kconfiglib.TRISTATE:
                    list_res += ["<" + conflict + "> -- "
                                 "Value (" + c.get_value() + ")"]
        return list_res

    def get_current_opt_verbose(self):
        """ Return a option's verbose output """
        return str(self.items[self.cursor])

    def get_all_sections(self):
        """ Return all kernel's sections into a list """
        return self.sections

    def goto_search_result(self, name):
        """ Goto method, go to the name's option if it exists"""
        result = re.search('<(.*)>', name)
        option_name = ""
        if result:
            option_name = result.group(1)

        cpt = 0
        find = False

        for i in self.items:
            if option_name != "":
                if option_name == i.get_name():
                    find = True
                    break
            else:
                # Choice
                if len(i.get_prompts()) > 0:
                    if name == i.get_prompts()[0]:
                        find = True
                        break
            cpt += 1
        if find:
            self.goto_opt(cpt)
            return 0
        else:
            return -1

    def goto_opt(self, opt_id):
        """ Goto method, go to the option 'opt_id'
        Increment the history save
        """
        if self.cursor != -1:
            self.history.append(self.cursor)
        self.cursor = opt_id

    def goto_back_is_possible(self):
        """ Return if we can go back """
        return len(self.history) >= 1

    def goto_back_opt(self):
        """Goto method, go to the previous option on history's save top
        Return 0 if it is done, else return -1 if it cannot be done
        """
        if self.goto_back_is_possible():
            self.cursor = self.history.pop()
        return self.goto_back_is_possible()

    def goto_next_opt(self):
        """ Goto method, go to the next symbol option
        (not menus/comment/string/hex..) which may be modified or not.
        Return True is we can go to the next option"""
        #A voir, test pour si valeur par défaut
        old_option = self.cursor

        if self.cursor != -1:
            self.history.append(self.cursor)

        if self.cursor < len(self.items):
            self.cursor += 1
            while 1:
                current_item = self.items[self.cursor]

                # Menu, comment, unknown, string, hex, int : skip

                if current_item.is_symbol():
                    if current_item.get_type() == kconfiglib.BOOL or \
                       current_item.get_type() == kconfiglib.TRISTATE:
                        break
                elif current_item.is_choice():
                    break
                self.cursor += 1

                if self.cursor >= len(self.items):
                    self.cursor = old_option
                    current_item = self.items[self.cursor]
                    self.history.pop()
                    return False

        return True

    def set_current_opt_value(self, value_user_cursor):
        """Set the current option's value with value_user_cursor ("y", "n",
            "m" (if tristate))
        In case of choice, if no choice is selected : value_user_cursor == "N"
        """
        current_item = self.items[self.cursor]

        if current_item.is_symbol():
            self.items[self.cursor].set_user_value(value_user_cursor)
        elif current_item.is_choice():
            items = current_item.get_symbols()
            for i in items:
                if value_user_cursor == "N":
                    # All choices clear
                    i.set_user_value("n")
                elif i.get_name() == value_user_cursor:
                    i.set_user_value("y")
                    break

    def get_tree_representation(self):
        """ Return in a structure,
        the current configuration's representation
        sc = symbol or choice
        [sc, sc, [menu, [sc], menu, [menu, [sc]]], sc]
        """
        return self._get_tree_representation_rec(self.top_level_items)

    def _get_tree_representation_rec(self, father):
        """ Private recursive fct
        see get_tree_representation()
        """
        res = []
        for i in father:
            if i.is_symbol():
                if i.get_type() == kconfiglib.BOOL or\
                        i.get_type() == kconfiglib.TRISTATE:
                    description = i.get_prompts()
                    name = "<" + i.get_name() + ">"
                    if description != []:
                        name = description[0] + " :: " + name
                    res += [name]
            elif i.is_choice():
                tmp = i.get_prompts()
                if len(tmp) > 0:
                    res += [str(tmp[0])]
            elif i.is_menu():
                res += [[i.get_title(),
                        self._get_tree_representation_rec(i.get_items())]]
        return res

    def search_options_from_pattern(self, pattern):
        """ Return a list of option's name found with a pattern """
        if type(pattern) is not str:
            return []
        elif pattern == "":
            return self.get_tree_representation()

        filtred = search.get_items_for_search(self.kconfig_infos)
        result_search = search.search_pattern(pattern, filtred)
        result_search = sorted(result_search)

        res = []

        for current_name, current_item in result_search:
            if current_item.is_choice() or current_item.is_symbol():
                description = current_item.get_prompts()

                option = "<" + current_name + ">"
                if description:
                    option = description[0] + " :: " + option

                res += [option]

        return res

    def finish_write_config(self, output_file):
        """ Finish the configuration, write the .config file """
        self.kconfig_infos.write_config(output_file)

    def get_symbol_condition(self):
        condition = ""

        # Zone prompt
        current_item = self.items[self.cursor]
        zonePrompts = str(current_item).split("Prompts:")[1].split(")")[0] + ")"

        if "if " in str(zonePrompts):
            cond_prompt = str(zonePrompts).split\
                                ("if ")[1].split(")")[0] + ")"
            #if cond_prompt != "(no reverse dependencies ":
            condition += "condition prompt : " + cond_prompt + "\n"

        # Zone Default
        if "Condition:" in str(current_item):
            cond_default = str(current_item).split\
                                ("Condition:")[1].split(")")[0] + ")"
            #if cond_default != "(none":
            condition += "condition default : " + cond_default + "\n"
                    
        # Zone Select
        if "Selects:" in str(current_item):
        
            zoneSelect = str(current_item).split("Selects:")\
                [1].split("Reverse dependencies:")[0]

            subZone = str(zoneSelect).split("\n")
            for cond in subZone:
                if "if " in str(cond):
                    condition += "condition select : " + \
                        str(cond).split("if ")[1] + "\n"

        # Zone Reverse
        if "Reverse dependencies:" in str(current_item):
        
            zoneReverse = str(current_item).split("Reverse dependencies:")\
                [1].split("Additional dependencies")[0]

            subZone = str(zoneReverse).split("\n")
            for cond in subZone:
                if cond != "":
                    condition += "condition reverse :" + str(cond) + "\n"


        # Zone Additional
        if "menu and if's:" in str(current_item):
            zoneAdditional = str(current_item).split("menus and if's:")\
                [1].split("Locations:")[0]

            subZone = str(zoneAdditional).split("\n")
            for cond in subZone:
                if cond != "":
                    condition += "condition additional :" + str(cond) + "\n"

        return condition
