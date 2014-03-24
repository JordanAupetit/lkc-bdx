#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import Gtk

import os
import sys
import re

import app_core


class ConfigurationInterface(Gtk.Window):
    def __init__(self, app_memory):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('interface/chooseConfiguration.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory
        self.input_choose_kernel = \
            self.interface.get_object("input_choose_kernel")
        self.input_choose_config = \
            self.interface.get_object("input_choose_config")
        self.btn_choose_config = \
            self.interface.get_object("btn_choose_config")
        self.combo_text_archi_folder = \
            self.interface.get_object("combo_text_archi_folder")
        self.combo_text_archi_defconfig = \
            self.interface.get_object("combo_text_archi_defconfig")
        self.radio_load = self.interface.get_object("radio_load")
        self.radio_state = "default"
        self.srcdefconfig = ""
        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        if (self.toClose):
            app_memory["open"] = False
        Gtk.main_quit()

    def on_btn_choose_kernel_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.input_choose_kernel.set_text(dialog.get_filename())
        dialog.destroy()

    def on_input_choose_kernel_changed(self, widget):
        path = self.input_choose_kernel.get_text()
        res = self.app_memory["kconfig_infos"].init_test_environnement(path)

        self.combo_text_archi_folder.remove_all()
        self.combo_text_archi_defconfig.remove_all()
        self.combo_text_archi_defconfig.set_sensitive(False)

        if res == -1:
            self.combo_text_archi_folder.set_sensitive(False)
            return

        self.combo_text_archi_folder.set_sensitive(True)

        for arch in res:
            self.combo_text_archi_folder.append_text(arch[0])

    def on_combo_text_archi_folder_changed(self, widget):
        arch_active = self.combo_text_archi_folder.get_active_text()

        if arch_active is not None:
            tmp = self.app_memory["kconfig_infos"].get_all_defconfig()

            for arch in tmp:
                if arch_active == arch[0]:
                    self.combo_text_archi_defconfig.set_sensitive(True)
                    self.combo_text_archi_defconfig.remove_all()
                    if type(arch[1]) is list:
                        for i in arch[1]:
                            self.combo_text_archi_defconfig.append_text(i)
                        break
                    else:
                        self.combo_text_archi_defconfig.append_text(arch[1])
                        break

    def on_btn_choose_config_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file",
                                       self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.input_choose_config.set_text(dialog.get_filename())

        dialog.destroy()

    def on_btn_help_default_clicked(self, widget):
        dialog = DialogHelp(self.window, "default")
        dialog.run()
        dialog.destroy()

    def on_btn_help_load_clicked(self, widget):
        dialog = DialogHelp(self.window, "load")
        dialog.run()
        dialog.destroy()

    def on_btn_stop_clicked(self, widget):
        print "Nothing"

    def on_btn_next_clicked(self, widget):
        if self.input_choose_kernel.get_text() == "" or\
                self.combo_text_archi_folder.get_active_text() is None or\
                self.combo_text_archi_defconfig.get_active_text() is None:
            dialog = DialogHelp(self.window, "error_load_kernel")
            dialog.run()
            dialog.destroy()
            return

        if self.radio_load.get_active():
            if self.input_choose_config.get_text() == "":
                dialog = DialogHelp(self.window, "error_load_config")
                dialog.run()
                dialog.destroy()
                return

        path = self.input_choose_kernel.get_text()

        if path[:-1] != "/":
            path += "/"

        arch = self.combo_text_archi_defconfig.get_active_text()
        srcarch = self.combo_text_archi_folder.get_active_text()

        load_config = ""
        if (self.radio_state == "default"):
            print("Configuration by default")
            load_config = ""
        elif (self.radio_state == "load"):
            print("Configuration by load")
            load_config = self.input_choose_config.get_text()

        app_memory["kconfig_infos"].init_memory(path,
                                                arch,
                                                srcarch,
                                                load_config)

        self.toClose = False
        app_memory["to_open"] = "OptionsInterface"
        self.window.destroy()

    def on_radio_default_released(self, widget):
        self.radio_state = "default"
        self.input_choose_config.set_sensitive(False)
        self.btn_choose_config.set_sensitive(False)

    def on_radio_load_released(self, widget):
        self.radio_state = "load"
        self.input_choose_config.set_sensitive(True)
        self.btn_choose_config.set_sensitive(True)

    def on_btn_exit_clicked(self, widget):
        self.window.destroy()


class OptionsInterface(Gtk.Window):
    def __init__(self, app_memory):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('interface/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory
        self.current_option_index = -1
        self.previous_options = []

        self.window.set_title("Linux Kernel Configuration - Architecture : " +
                              app_memory["kconfig_infos"].get_srcarch())

        # For tree displaying
        self.treestore_search = Gtk.TreeStore(str)
        self.treeview_search = Gtk.TreeView(model=self.treestore_search)

        self.treestore_section = Gtk.TreeStore(str)
        self.treeview_section = Gtk.TreeView(model=self.treestore_section)

        self.treestore_conflicts = Gtk.TreeStore(str)
        self.treeview_conflicts = Gtk.TreeView(model=self.treestore_conflicts)

        # Cursor list options
        self.move_cursor_search_allowed = True
        self.move_cursor_section_allowed = True
        self.move_cursor_conflicts_allowed = True

        self.label_title_option = \
            self.interface.get_object("label_title_option")
        self.radio_yes = self.interface.get_object("radio_yes")
        self.radio_module = self.interface.get_object("radio_module")
        self.radio_no = self.interface.get_object("radio_no")
        self.combo_choice = self.interface.get_object("combo_choice")
        self.label_description_option = \
            self.interface.get_object("label_description_option")
        self.btn_back = self.interface.get_object("btn_back")
        self.btn_next = self.interface.get_object("btn_next")
        self.input_search = self.interface.get_object("input_search")
        self.list_options = self.interface.get_object("list_options")
        self.label_current_menu = self.interface.get_object("label_current_menu")
        self.notebook = self.interface.get_object("notebook2")

        self.btn_back.set_sensitive(False)

        self.add_tree_view()
        # Initialisation de l'arbre des options
        self.get_tree_option(self.top_level_items)
        self.add_section_tree()
        self.add_conflicts_tree()

        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            app_memory["open"] = False
        Gtk.main_quit()

    def on_btn_back_clicked(self, widget):
        tmp = self.app_memory["kconfig_infos"].goto_back_opt()
        if tmp == -1:
            self.btn_back.set_sensitive(False)
        elif tmp == 0:
            self.btn_right.set_sensitive(True)
            self.change_option()

    def on_btn_next_clicked(self, widget):
        self.set_value_option()
        old_position = self.current_option_index
        if self.current_option_index >= 0:
            self.previous_options.append(self.current_option_index)

        self.current_option_index += 1
        show = False

        self.show_interface_option()

        while show is False:
            if(self.current_option_index > (len(self.items) - 1)):
                self.current_option_index = old_position
                self.btn_next.set_sensitive(False)
                self.previous_options.pop()

            current_item = self.items[self.current_option_index]

            if current_item.is_symbol():
                if (current_item.get_type() == kconfiglib.BOOL or
                    current_item.get_type() == kconfiglib.TRISTATE):
                    show = True
                else:
                    self.current_option_index += 1
                    print("Symbol but not Bool or Tristate")
            if current_item.is_menu():
                self.current_option_index += 1
                print("NEXT CLICKED #SKIP# -- Menu")
            if current_item.is_choice():
                show = True
            if current_item.is_comment():
                self.current_option_index += 1
                print("NEXT CLICKED #SKIP# -- Comment")

        if len(self.previous_options) > 0:
            self.btn_back.set_sensitive(True)
        self.change_option()

    def set_value_option(self):
        current_item = self.items[self.current_option_index]

        if current_item.is_symbol():
            if self.radio_yes.get_active():
                self.items[self.current_option_index].set_user_value("y")
            elif self.radio_module.get_active():
                self.items[self.current_option_index].set_user_value("m")
            elif self.radio_no.get_active():
                self.items[self.current_option_index].set_user_value("n")
        elif current_item.is_choice():
            value = self.combo_choice.get_active_text()
            items = current_item.get_symbols()
            if value == "No choice are selected":
                for i in items:
                    i.set_user_value("n")
            else:
                for i in items:
                    if i.get_name() == value:
                        i.set_user_value("y")

        if not app_memory["modified"]:
            app_memory["modified"] = True

    def show_interface_option(self):
        self.radio_yes.set_visible(True)
        self.radio_module.set_visible(True)
        self.radio_no.set_visible(True)

    def on_radio_yes_released(self, widget):
        self.change_interface_conflit("y")

    def on_radio_module_released(self, widget):
        self.change_interface_conflit("m")

    def on_radio_no_released(self, widget):
        self.change_interface_conflit("n")

    def change_interface_conflit(self, radio_type):
        self.btn_next.set_sensitive(True)
        self.move_cursor_conflicts_allowed = False
        self.treestore_conflicts.clear()
        self.move_cursor_conflicts_allowed = True

        if self.items[self.current_option_index].get_value() != radio_type and\
                self.items[self.current_option_index].is_modifiable() is False:
            self.btn_next.set_sensitive(False)

            local_opt_name = self.items[self.current_option_index].get_name()
            cur_opt = utility.SymbolAdvance(self.app_memory["kconfig_infos"]
                                                .get_symbol(local_opt_name))

            string_symbol_list = str(cur_opt.cat_symbols_list())
            list_conflicts = cur_opt.cat_symbols_list()

            for conflit in list_conflicts:

                cpt = 0
                find = False

                for item in self.items:
                    if(conflit == item.get_name()):
                        find = True
                        break
                    cpt += 1

                print "CPT => " + str(cpt)

                # FIXME on ne traite que les symbols
                if (find and (self.items[cpt].get_type() == kconfiglib.BOOL or\
                        self.items[cpt].get_type() == kconfiglib.TRISTATE)):

                    self.treestore_conflicts.append(None,
                                                    ["<" + conflit
                                                         + "> -- Value("
                                    + str(self.items[cpt].get_value()) + ")"])
                else:
                    print "CONFLICT not bool or tristate"

            if list_conflicts != []:
                # 2 => Conflicts page
                self.notebook.set_current_page(2)

        if radio_type == "?":
            self.btn_next.set_sensitive(True)

    def on_combo_choice_changed(self, widget):
        self.btn_next.set_sensitive(True)
        current_item = self.items[self.current_option_index]
        active_text = self.combo_choice.get_active_text()
        selection = current_item.get_selection()

        if current_item.get_visibility() == "n":
            if selection is None:
                if active_text == "No choice are selected":
                    return
                else:
                    self.btn_next.set_sensitive(False)
            else:
                for i in current_item.get_symbols():
                    if i.get_value() == "y" and i.get_name() != active_text:
                        self.btn_next.set_sensitive(False)

    def on_btn_search_clicked(self, widget):
        self.search_options()

    def on_input_search_activate(self, widget):
        self.search_options()

    def on_btn_clean_search_clicked(self, widget):
        self.get_tree_option(self.top_level_items)
        self.input_search.set_text("")
        print "Cleaned !"

    # PAS TOUCHE KNR
    def search_options(self):
        pattern = self.input_search.get_text()

        if pattern == "":
            self.get_tree_option(self.top_level_items)
            return

        filtred = search.get_items_for_search(app_memory["kconfig_infos"])
        r = search.search_pattern(pattern, filtred);
        r = sorted(r)

        i = 0
        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        for current_name, current_item in r:
            if current_item.is_choice() or current_item.is_symbol():
                description = current_item.get_prompts()

                option = "<" + current_name + ">"
                if description:
                    option = description[0] + " :: " + option
                self.treestore_search.append(None, [option])
                i += 1

        title = "Matching option"
        if i > 1:
            title += "s"

        title += " : " + str(i)

        self.change_title_column_treeview(title, 0)

    def get_tree_option(self, items, parent=None):
        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        self.change_title_column_treeview("Complete list of options : " +
                                          str(len(self.items)), 0)
        self.get_tree_options_rec(items, parent)

    def get_tree_options_rec(self, items, parent):
        for item in items:
            if item.is_symbol():
                if (item.get_type() == kconfiglib.BOOL or
                    item.get_type() == kconfiglib.TRISTATE):

                    description = item.get_prompts()
                    name = item.get_name()
                    option = "<" + name + ">"
                    if description:
                        option = description[0] + " :: " + option
                    self.treestore_search.append(parent, [option])
            elif item.is_menu():
                menu = self.treestore_search.append(parent, [item.get_title()])
                self.get_tree_options_rec(item.get_items(), menu)
            elif item.is_choice():
                if len(item.get_prompts()) > 0:
                    self.treestore_search.append(parent,
                                                 [str(item.get_prompts()[0])])

    def on_btn_finish_clicked(self, widget):
        self.app_memory["kconfig_infos"].write_config(".config")
        self.window.destroy()

    def change_option(self):
        help_text = self.app_memory["kconfig_infos"].get_current.opt_help()

        if help_text is not None:
            self.label_description_option.set_text(help_text)
        else:
            self.label_description_option.set_text("No help available.")

        self.move_cursor_section_allowed = False

        index_menu_option =\
            self.app_memory["kconfig_infos"].get_current_opt_parent_topmenu()
        self.treeview_section.set_cursor(index_menu_option)

        self.move_cursor_section_allowed = True
        self.label_current_menu.set_visible(True)
        menu_str = self.app_memory["kconfig_infos"]\
                       .get_current_opt_parent_topmenu_str()
        self.label_current_menu.set_text(menu_str)

        current_item = self.items[self.current_option_index]

        if self.app_memory["kconfig_infos"].is_current_opt_symbol():
            index = self.app_memory["kconfig_infos"].get_current_opt_index()
            name = self.app_memory["kconfig_infos"].get_current_opt_name()
            value = self.app_memory["kconfig_infos"].get_current_opt_value()

            text = "[Option n°" + str(index) + "] "
            text += "Do you want " + name + " option enabled ?"
            self.label_title_option.set_text(text)

            if value == "y":
                self.radio_yes.set_active(True)
            if value == "m":
                self.radio_module.set_active(True)
            if value == "n":
                self.radio_no.set_active(True)

            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)
            self.combo_choice.set_visible(False)

            # Enabling few radio button
            type_b = self.app_memory["kconfig_infos"].is_current_opt_bool()
            type_t = self.app_memory["kconfig_infos"].is_current_opt_tristate()
            if type_b is True:
                self.radio_yes.set_visible(True)
                self.radio_no.set_visible(True)
            elif type_t is True:
                self.radio_yes.set_visible(True)
                self.radio_module.set_visible(True)
                self.radio_no.set_visible(True)

        elif self.app_memory["kconfig_infos"].is_current_opt_choice():
            if len(current_item.get_prompts()) > 0:
                text = "[Option n°" + str(self.current_option_index) + "] "
                text += "Do you want to change the selected option of this choice ? \n"
                text += current_item.get_prompts()[0]
                self.label_title_option.set_text(text)
            else:
                self.label_title_option \
                .set_text("[Option n°" + str(self.current_option_index) + \
                    "] Do you want to change the selected option of this choice ?")


            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)

            self.combo_choice.set_visible(True)

            self.combo_choice.remove_all()

            self.combo_choice.append_text("No choice are selected")
            self.combo_choice.set_active(0)

            combo_setted = False
            index = 1
            for item in current_item.get_symbols():
                self.combo_choice.append_text(item.get_name())
                if item.get_value() == "y":
                    self.combo_choice.set_active(index)
                    combo_setted = True
                index += 1

            if combo_setted:
                self.combo_choice.remove(0)

    def change_title_column_treeview(self, title, id_column):
        column = self.treeview_search.get_column(id_column)
        column.set_title(title)

    def add_tree_view(self, title="List of options"):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(title, renderer_text, text=0)
        self.treeview_search.append_column(column_text)
        self.treeview_search.set_enable_search(False)
        self.treeview_search.connect("cursor-changed",
                                     self.on_cursor_treeview_search_changed)

        scrolledwindow_search = self.interface.get_object("scrolledwindow_search")
        scrolledwindow_search.add(self.treeview_search)
        scrolledwindow_search.show_all()

    def add_section_tree(self):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Sections", renderer_text, text=0)
        self.treeview_section.append_column(column_text)
        self.treeview_section.set_enable_search(False)
        self.treeview_section.connect("cursor-changed",
                                      self.on_cursor_treeview_section_changed)

        scrolledwindow_section = self.interface.get_object("scrolledwindow_section")
        scrolledwindow_section.add(self.treeview_section)

        self.treestore_section.append(None,
                                      ["General options (options without menu)"])

        for m in self.top_menus:
            self.treestore_section.append(None, [m.get_title()])

        scrolledwindow_section.show_all()

    def add_conflicts_tree(self):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Conflicts", renderer_text, text=0)
        self.treeview_conflicts.append_column(column_text)
        self.treeview_conflicts.set_enable_search(False)
        self.treeview_conflicts.connect("cursor-changed",
                                     self.on_cursor_treeview_conflicts_changed)

        scrolledwindow_conflicts = self.interface.get_object("scrolledwindow_conflicts")
        scrolledwindow_conflicts.add(self.treeview_conflicts)

        scrolledwindow_conflicts.show_all()

    def on_cursor_treeview_search_changed(self, widget):
        if self.move_cursor_search_allowed:
            # Only one column
            current_column = 0

            if not widget.get_selection():
                return

            (treestore, index) = widget.get_selection().get_selected()

            if index is not None:
                option_description = treestore[index][current_column]

                result = re.search('<(.*)>', option_description)
                option_name = ""
                if result:
                    option_name = result.group(1)

                cpt = 0
                find = False

                for item in self.items:
                    if(option_name != ""):
                        if(option_name == item.get_name()):
                            find = True
                            break
                    else:
                        # Choice
                        if len(item.get_prompts()) > 0:
                            if option_description == item.get_prompts()[0]:
                                find = True
                                break
                    cpt += 1
                if find:
                    if self.current_option_index >= 0:
                        self.previous_options.append(self.current_option_index)

                    if len(self.previous_options) > 0:
                        self.btn_back.set_sensitive(True)

                    self.current_option_index = cpt
                    self.btn_next.set_sensitive(True)
                    self.change_option()

    def on_cursor_treeview_section_changed(self, widget):
        if self.move_cursor_section_allowed:
            if not widget.get_selection():
                    return

            # Only one column
            current_column = 0
            (treestore, index) = widget.get_selection().get_selected()

            if index is not None:
                menu_title = treestore[index][current_column]

                cpt = 0
                find = False

                if menu_title == "General options (options without menu)":
                    cpt = -1
                    find = True
                else:
                    for menu in self.top_menus:
                        if(menu_title == menu.get_title()):
                            find = True
                            break
                        cpt += 1

                if find:
                    first_option_index_menu = 0

                    if cpt == -1:
                        first_option_index_menu = utility.get_first_option_menu(\
                            None, self.items)
                    else:
                        first_option_index_menu = utility.get_first_option_menu(\
                                self.top_menus[cpt], self.items)

                    if self.current_option_index >= 0:
                        self.previous_options.append(self.current_option_index)

                    if len(self.previous_options) > 0:
                        self.btn_back.set_sensitive(True)

                    self.current_option_index = first_option_index_menu
                    self.btn_next.set_sensitive(True)
                    self.change_option()

    def on_cursor_treeview_conflicts_changed(self, widget):
        if self.move_cursor_conflicts_allowed:
            # Only one column
            current_column = 0
            if not widget.get_selection():
                return

            (treestore, index) = widget.get_selection().get_selected()

            if index is not None:
                option_description = treestore[index][current_column]

                result = re.search('<(.*)>', option_description)
                option_name = ""
                if result:
                    option_name = result.group(1)

                cpt = 0
                find = False

                for item in self.items:
                    if(option_name == item.get_name()):
                        find = True
                        break
                    cpt += 1

                if find:
                    if self.current_option_index >= 0:
                        self.previous_options.append(self.current_option_index)

                    if len(self.previous_options) > 0:
                        self.btn_back.set_sensitive(True)

                    self.current_option_index = cpt
                    self.btn_next.set_sensitive(True)
                    self.change_option()

                    self.move_cursor_conflicts_allowed = False
                    self.treestore_conflicts.clear()
                    self.move_cursor_conflicts_allowed = True

    # MENUBAR
    def on_menu1_new_activate(self, widget):
        print "new"

    def on_menu1_open_activate(self, widget):
        print "open"

    def on_menu1_save_activate(self, widget):
        if app_memory["new_config"]:
            app_memory["new_config"] = False
            self.on_menu1_save_as_activate(widget)
        else:
            save_path = app_memory["save_path"]
            config_name = app_memory["config_name"]

            app_memory["kconfig_infos"].write_config(save_path + config_name)

            if app_memory["modified"] is True:
                app_memory["modified"] = False

    def on_menu1_save_as_activate(self, widget):
        save_path = app_memory["save_path"]
        config_name = app_memory["config_name"]

        save_as_dialog = Gtk.FileChooserDialog("Save as", self,
                                        Gtk.FileChooserAction.SAVE,
                                        ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Save", Gtk.ResponseType.OK))

        save_as_dialog.set_filename(save_path + config_name)
        save_as_dialog.set_do_overwrite_confirmation(True)

        response = save_as_dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = save_as_dialog.get_filename()
            config_name = save_as_dialog.get_current_name()

            l = len(filename) - len(config_name)
            save_path = filename[0:l]

            app_memory["kconfig_infos"].write_config(save_path + config_name)
            app_memory["save_path"] = save_path
            app_memory["config_name"] = config_name

            if app_memory["modified"] is True:
                app_memory["modified"] = False
        save_as_dialog.destroy()

    def on_menu1_quit_activate(self, widget):
        if app_memory["modified"]:
            save_btn = "Save"
            label = Gtk.Label("Do you want to save the modification of the " +
                              "kernel configuration file" +
                              " «" + app_memory["config_name"] + "» " +
                              "before to close?")

            if app_memory["new_config"]:
                save_btn += " as"

            quit_dialog = Gtk.Dialog("Exit", self, 0,
                                    ("Exit whitout save", Gtk.ResponseType.NO,
                                     "Cancel", Gtk.ResponseType.CANCEL,
                                     save_btn, Gtk.ResponseType.YES))
            box = quit_dialog.get_content_area()
            box.add(label)
            quit_dialog.show_all()

            response = quit_dialog.run()

            if response == Gtk.ResponseType.YES:
                if app_memory["new_config"]:
                    self.on_menu1_save_as_activate(widget)
                else:
                    self.on_menu1_save_activate(widget)
                quit_dialog.destroy()
                self.on_mainWindow_destroy(widget)
            elif response == Gtk.ResponseType.NO:
                quit_dialog.destroy()
                self.on_mainWindow_destroy(widget)
            else:
                quit_dialog.destroy()
        else:
            self.on_mainWindow_destroy(widget)

        #app_memory["kconfig_infos"].write_config(".config")
        #self.window.destroy()

    # TOOLBAR
    def on_new_button_clicked(self, widget):
        self.on_menu1_new_activate(widget)

    def on_open_button_clicked(self, widget):
        self.on_menu1_open_activate(widget)

    def on_save_button_clicked(self, widget):
        self.on_menu1_save_activate(widget)

    def on_save_as_button_clicked(self, widget):
        self.on_menu1_save_as_activate(widget)

    def on_expand_button_clicked(self, widget):
        self.treeview_search.expand_all()

    def on_collapse_button_clicked(self, widget):
        self.treeview_search.collapse_all()


class DialogHelp(Gtk.Dialog):
    def __init__(self, parent, text_type):
        Gtk.Dialog.__init__(self, "Information", parent, 0, (Gtk.STOCK_OK,
                                                            Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Erreur")

        if (text_type == "default"):
            label = Gtk.Label("DEFAULT -- This is a dialog to \
display additional information ")
        elif (text_type == "load"):
            label = Gtk.Label("LOAD -- This is a dialog to \
display additional information ")
        elif (text_type == "error_load_kernel"):
            label = Gtk.Label("Error -- You haven't completed the Linux \
Kernel field \n and/or the Architecture field.")
        elif (text_type == "error_load_config"):
            label = Gtk.Label("Error --  You haven't completed the \
Config to load field")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


# ===========
# == DEBUG ==
def print_with_indent(s, indent):
    print (" " * indent) + s


# ===========
# == DEBUG ==
def print_items(items, indent):
    for item in items:
        if item.is_symbol():
            print_with_indent("config {0}".format(item.get_name()), indent)
        elif item.is_menu():
            print_with_indent('menu "{0}"'.format(item.get_title()), indent)
            print_items(item.get_items(), indent + 2)
        elif item.is_choice():
            print_with_indent('choice', indent)
            print_items(item.get_items(), indent + 2)
        elif item.is_comment():
            print_with_indent('comment "{0}"'.format(item.get_text()), indent)

if __name__ == "__main__":
    app_memory = {}
    app_memory["kernel_path"] = ""
    app_memory["archi_folder"] = ""
    app_memory["archi_defconfig"] = ""

    if len(sys.argv) >= 2:
        if os.path.exists(sys.argv[1]):
            path = sys.argv[1]
            if path[len(path)-1] != "/":
                path += "/"
            app_memory["kernel_path"] = path

        if len(sys.argv) >= 3:
            path = app_memory["kernel_path"] + "arch/" + sys.argv[2] + "/"
            if path[len(path)-1] != "/":
                path += "/"
            if os.path.exists(path):
                app_memory["archi_folder"] = sys.argv[2]

                if len(sys.argv) >= 4:
                    if os.path.exists(path + "configs/"):
                        path += "configs/"
                    if os.path.exists(path + sys.argv[3]):
                        app_memory["archi_defconfig"] = sys.argv[3]
                        print app_memory["archi_defconfig"]

    app_memory["open"] = True
    app_memory["to_open"] = "ConfigurationInterface"

    app_memory["save_path"] = app_memory["kernel_path"]
    app_memory["config_name"] = ".config"
    app_memory["modified"] = True
    app_memory["new_config"] = True

    app_memory["kconfig_infos"] = app_core.AppCore()
    while(app_memory["open"]):
        if (app_memory["to_open"] == "ConfigurationInterface"):
            ConfigurationInterface(app_memory)
            Gtk.main()
        elif (app_memory["to_open"] == "OptionsInterface"):
            OptionsInterface(app_memory)
            Gtk.main()


"""
Faire une grosse classe MAIN qui ouvre les fenetres
Qui récupère les valeurs de retours de fenetre pour en ouvrir d'autres
Et cette classe stockera les informations nécessaire a l'application
(options, option courante, ...)
"""
