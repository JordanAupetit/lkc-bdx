#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk

import os
import sys
import re

import app_core


class ConfigurationInterface(gtk.Window):
    def __init__(self, app_memory):
        self.interface = gtk.Builder()
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
        self.btn_next = self.interface.get_object("btn_next")
        self.radio_state = "default"
        self.srcdefconfig = ""
        self.interface.connect_signals(self)

        if app_memory["kernel_path"] != "":
            self.input_choose_kernel.set_text(app_memory["kernel_path"])

    def on_mainWindow_destroy(self, widget):
        if (self.toClose):
            app_memory["open"] = False
        gtk.main_quit()

    def on_btn_choose_kernel_clicked(self, widget):
        dialog = gtk.FileChooserDialog("Please choose a folder", self,
                                       gtk.FileChooserAction.SELECT_FOLDER,
                                       ("Cancel", gtk.ResponseType.CANCEL,
                                        "Select", gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == gtk.ResponseType.OK:
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

        i_archi_folder = 0
        i = 0
        for arch in res:
            self.combo_text_archi_folder.append_text(arch[0])
            i += 1
            if arch[0] == self.app_memory["archi_folder"]:
                i_archi_folder = i - 1

        self.combo_text_archi_folder.set_active(i_archi_folder)

    def on_combo_text_archi_folder_changed(self, widget):
        arch_active = self.combo_text_archi_folder.get_active_text()

        if arch_active is not None:
            tmp = self.app_memory["kconfig_infos"].get_all_defconfig()

            i_defconfig = 0
            j = 0
            next_auto = False

            for arch in tmp:
                if arch_active == arch[0]:
                    self.combo_text_archi_defconfig.set_sensitive(True)
                    self.combo_text_archi_defconfig.remove_all()
                    if type(arch[1]) is list:
                        for i in arch[1]:
                            self.combo_text_archi_defconfig.append_text(i)
                            j += 1
                            if i == self.app_memory["archi_defconfig"]:
                                i_defconfig = j - 1
                                next_auto = True
                        break
                    else:
                        self.combo_text_archi_defconfig.append_text(arch[1])
                        i_defconfig = 0
                        break

            self.combo_text_archi_defconfig.set_active(i_defconfig)
            if next_auto is True and self.app_memory["archi_config"] == "":
                #self.on_btn_next_clicked(self.btn_next)
                pass

    def on_btn_choose_config_clicked(self, widget):
        dialog = gtk.FileChooserDialog("Please choose a file",
                                       self,
                                       gtk.FileChooserAction.OPEN,
                                       (gtk.STOCK_CANCEL,
                                        gtk.ResponseType.CANCEL,
                                        "Select", gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == gtk.ResponseType.OK:
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

        if path[-1] != "/":
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
            print load_config

        app_memory["kconfig_infos"].init_memory(path,
                                                arch,
                                                srcarch,
                                                load_config)

        self.toClose = False
        app_memory["to_open"] = "OptionsInterface"

        
        
        self.window.destroy()

    def on_radio_default_clicked(self, widget):
        self.radio_state = "default"
        self.input_choose_config.set_sensitive(False)
        self.btn_choose_config.set_sensitive(False)

    def on_radio_load_clicked(self, widget):
        self.radio_state = "load"
        self.input_choose_config.set_sensitive(True)
        self.btn_choose_config.set_sensitive(True)

    def on_btn_exit_clicked(self, widget):
        self.window.destroy()


class OptionsInterface(gtk.Window):
    def __init__(self, app_memory):
        self.first_next = True

        self.interface = gtk.Builder()
        self.interface.add_from_file('interface/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory

        self.window.set_title("Linux Kernel Configuration - Architecture : " +
                              app_memory["kconfig_infos"].get_srcarch())

        # For tree displaying
        self.treestore_search = gtk.TreeStore(str)
        self.treeview_search = gtk.TreeView(model=self.treestore_search)

        self.treestore_section = gtk.TreeStore(str)
        self.treeview_section = gtk.TreeView(model=self.treestore_section)

        self.treestore_conflicts = gtk.TreeStore(str)
        self.treeview_conflicts = gtk.TreeView(model=self.treestore_conflicts)

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

        self.save_toolbar = self.interface.get_object('save_button')
        self.save_menubar = self.interface.get_object('menu1_save')        

        self.btn_back.set_sensitive(False)

        self.add_tree_view()
        # Initialisation de l'arbre des options
        self.get_tree_option()
        self.add_section_tree()
        self.add_conflicts_tree()

        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            app_memory["open"] = False
        gtk.main_quit()

    def on_btn_back_clicked(self, widget):
        tmp = self.app_memory["kconfig_infos"].goto_back_opt()
        if tmp is False:
            self.btn_back.set_sensitive(False)
        elif tmp is True:
            self.btn_back.set_sensitive(True)
        self.change_option()
        self.change_interface_conflit("n")

    def on_btn_next_clicked(self, widget):

        #print "DEBUG FABIEN 1" 

        if self.first_next is True:
            self.first_next = False
            self.app_memory["kconfig_infos"].goto_next_opt()
            self.change_option()
            return

        self._set_value()
        self.app_memory["kconfig_infos"].goto_next_opt()

        if not app_memory["modified"]:
            app_memory["modified"] = True

        self.radio_yes.set_visible(True)
        self.radio_module.set_visible(True)
        self.radio_no.set_visible(True)

        # ---------------------------------------

        
        app_memory["kconfig_infos"].print_symbol_condition()

        self.change_interface_conflit("n")

        
        # ---------------------------------------

        if self.app_memory["kconfig_infos"].goto_back_is_possible() is True:
            self.btn_back.set_sensitive(True)

        self.change_option()



    def _set_value(self):
        if self.app_memory["kconfig_infos"].is_current_opt_symbol():
            value = self.app_memory["kconfig_infos"].get_current_opt_value()
            if self.radio_yes.get_active():
                value = "y"
            elif self.radio_module.get_active():
                value = "m"
            elif self.radio_no.get_active():
                value = "n"
        elif self.app_memory["kconfig_infos"].is_current_opt_choice():
            symbol_selected = self.combo_choice.get_active_text()
            if symbol_selected == "No choice are selected":
                value = "N"
            else:
                value = "symbol_selected"

        self.app_memory["kconfig_infos"].set_current_opt_value(value)

        if not app_memory["modified"]:
            app_memory["modified"] = True

        self.save_toolbar.set_sensitive(True)
        self.save_menubar.set_sensitive(True)

    def on_radio_yes_clicked(self, widget):
        self.change_interface_conflit("y")

    def on_radio_module_clicked(self, widget):
        self.change_interface_conflit("m")

    def on_radio_no_clicked(self, widget):
        self.change_interface_conflit("n")

    def change_interface_conflit(self, radio_type):
        self.btn_next.set_sensitive(True)
        self.move_cursor_conflicts_allowed = False
        self.treestore_conflicts.clear()
        self.move_cursor_conflicts_allowed = True
        self.radio_yes.set_sensitive(True)
        self.radio_no.set_sensitive(True)
        self.radio_module.set_sensitive(True)
        
        old = self.app_memory["kconfig_infos"].get_current_opt_value()
        modifiable = self.app_memory["kconfig_infos"].is_current_opt_modifiable()

        #if value != radio_type and modifiable is False:

        #self.app_memory["kconfig_infos"].is_current_opt_choice():
        #self.app_memory["kconfig_infos"].set_current_opt_value(value)

        self.app_memory["kconfig_infos"].set_current_opt_value("y")
        value = self.app_memory["kconfig_infos"].get_current_opt_value()
            
        if value != "y":
            self.radio_yes.set_sensitive(False)
            self.radio_module.set_sensitive(False)

        self.app_memory["kconfig_infos"].set_current_opt_value("n")
        value = self.app_memory["kconfig_infos"].get_current_opt_value()

        if value != "n":
            self.radio_no.set_sensitive(False)
        
        list_conflicts = self.app_memory["kconfig_infos"]\
            .get_current_opt_conflict()

        if list_conflicts != []:
            # 2 => Conflicts page
            #self.notebook.set_current_page(2)
            for conflict in list_conflicts:
                self.treestore_conflicts.append(None, [conflict])

        if radio_type == "?":
            self.btn_next.set_sensitive(True)

                    
    def on_combo_choice_changed(self, widget):
        active_text = self.combo_choice.get_active_text()

        if active_text == "No choice are selected":
            self.btn_next.set_sensitive(True)
            return

        res = self.app_memory["kconfig_infos"]\
                  .is_selection_opt_choice_possible(active_text)
        if res is not None:
            self.btn_next.set_sensitive(res)

    def on_btn_search_clicked(self, widget):
        self.search_options()

    def on_input_search_activate(self, widget):
        self.search_options()

    def on_btn_clean_search_clicked(self, widget):
        self.get_tree_option(self.top_level_items)
        self.input_search.set_text("")
        print "Cleaned !"

    def search_options(self):
        pattern = self.input_search.get_text()

        result_search = self.app_memory["kconfig_infos"]\
                            .search_options_from_pattern(pattern)

        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        title = "Matching option"
        if len(result_search) > 1:
            title += "s"

        title += " : " + str(len(result_search))
        self.change_title_column_treeview(title, 0)
        self._get_tree_option_rec(result_search, None)

    def get_tree_option(self):
        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        nb = self.app_memory["kconfig_infos"].get_number_options()
        self.change_title_column_treeview("Complete list of options : " +
                                          str(nb), 0)

        t = self.app_memory["kconfig_infos"].get_tree_representation()
        self._get_tree_option_rec(t, None)

    def _get_tree_option_rec(self, tree, parent):
        for i in tree:
            if type(i) is list:
                if len(i) == 1:
                    self.treestore_search.append(parent, [i[0]])
                elif len(i) == 2:
                    menu = self.treestore_search.append(parent, [i[0]])
                    self._get_tree_option_rec(i[1], menu)
            else:
                self.treestore_search.append(parent, [i])

    def on_btn_finish_clicked(self, widget):
        self.on_menu1_quit_activate(widget)

    def change_option(self):
        help_text = self.app_memory["kconfig_infos"].get_current_opt_help()
        self.label_description_option.set_text(help_text)

        self.move_cursor_section_allowed = False
        index_menu_option =\
            self.app_memory["kconfig_infos"].get_current_opt_parent_topmenu()
        self.treeview_section.set_cursor(index_menu_option)
        self.move_cursor_section_allowed = True

        self.label_current_menu.set_visible(True)
        menu_str = self.app_memory["kconfig_infos"]\
                       .get_current_opt_parent_topmenu_str()
        self.label_current_menu.set_text(menu_str)

        index = self.app_memory["kconfig_infos"].get_current_opt_index()

        if self.app_memory["kconfig_infos"].is_current_opt_symbol():
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
            prompt = self.app_memory["kconfig_infos"].get_current_opt_prompt()
            text = "[Option n°" + str(index) + "] "
            text += "Do you want to change the selected option of this choice ? \n"

            if len(prompt) > 0:
                text += prompt[0]

            self.label_title_option.set_text(text)

            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)

            self.combo_choice.set_visible(True)
            self.combo_choice.remove_all()
            self.combo_choice.append_text("No choice are selected")
            self.combo_choice.set_active(0)

            combo_setted = False
            index_combo = 1

            symbols_name = self.app_memory["kconfig_infos"]\
                               .get_current_choice_symbols_name()

            for item, value in symbols_name:
                self.combo_choice.append_text(item)
                if value == "y":
                    self.combo_choice.set_active(index_combo)
                    combo_setted = True
                index_combo += 1

            if combo_setted:
                self.combo_choice.remove(0)

    def change_title_column_treeview(self, title, id_column):
        column = self.treeview_search.get_column(id_column)
        column.set_title(title)

    def add_tree_view(self, title="List of options"):
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn(title, renderer_text, text=0)
        self.treeview_search.append_column(column_text)
        self.treeview_search.set_enable_search(False)
        self.treeview_search.connect("cursor-changed",
                                     self.on_cursor_treeview_search_changed)

        scrolledwindow_search = self.interface.get_object("scrolledwindow_search")
        scrolledwindow_search.add(self.treeview_search)
        scrolledwindow_search.show_all()

    def add_section_tree(self):
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Sections", renderer_text, text=0)
        self.treeview_section.append_column(column_text)
        self.treeview_section.set_enable_search(False)
        self.treeview_section.connect("cursor-changed",
                                      self.on_cursor_treeview_section_changed)

        scrolledwindow_section = self.interface.get_object("scrolledwindow_section")
        scrolledwindow_section.add(self.treeview_section)

        self.treestore_section.append(None,
                                      ["General options (options without menu)"])

        top_menus = self.app_memory["kconfig_infos"].get_all_topmenus_name()
        for m in top_menus:
            self.treestore_section.append(None, [m])

        scrolledwindow_section.show_all()

    def add_conflicts_tree(self):
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Conflicts", renderer_text, text=0)
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

                res = self.app_memory["kconfig_infos"]\
                          .goto_search_result(option_description)

                if res == 0:
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
                    menus = self.app_memory["kconfig_infos"].get_all_topmenus_name()
                    for menu in menus:
                        if menu_title == menu:
                            find = True
                            break
                        cpt += 1
                if find:
                    first_option_index_menu = 0

                    if cpt == -1:
                        first_option_index_menu =\
                                self.app_memory["kconfig_infos"]\
                                    .get_first_option_menu()
                    else:
                        first_option_index_menu =\
                                self.app_memory["kconfig_infos"]\
                                    .get_id_option_menu(cpt)

                    self.app_memory["kconfig_infos"]\
                        .goto_opt(first_option_index_menu)

                    #####
                    if self.app_memory["kconfig_infos"].goto_back_is_possible():
                        self.btn_back.set_sensitive(True)

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

                res = self.app_memory["kconfig_infos"]\
                          .goto_search_result(option_description)

                if res == 0:
                    #######
                    self.btn_next.set_sensitive(True)
                    self.change_option()

                    self.move_cursor_conflicts_allowed = False
                    self.treestore_conflicts.clear()
                    self.move_cursor_conflicts_allowed = True

    # MENUBAR
    def on_menu1_new_activate(self, widget):
        print "new"
        self.toClose = False
        if self.on_menu1_quit_activate(widget):
            self.window.destroy()
            app_memory["to_open"] = "ConfigurationInterface"
            gtk.main_quit()

    def on_menu1_save_activate(self, widget):
        if app_memory["new_config"]:
            self.on_menu1_save_as_activate(widget)
        else:
            save_path = app_memory["save_path"]
            config_name = app_memory["config_name"]

            app_memory["kconfig_infos"].finish_write_config(save_path + config_name)

            if app_memory["modified"] == True:
                app_memory["modified"] = False
                
            self.save_toolbar.set_sensitive(False)
            self.save_menubar.set_sensitive(False)
            
        """
        if app_memory["new_config"]:
            app_memory["new_config"] = False
            self.on_menu1_save_as_activate(widget)
        else:
            save_path = app_memory["save_path"]
            config_name = app_memory["config_name"]

            app_memory["kconfig_infos"].write_config(save_path + config_name)

            if app_memory["modified"] is True:
                app_memory["modified"] = False
        """

    def on_menu1_save_as_activate(self, widget):
        save_path = app_memory["save_path"]
        config_name = app_memory["config_name"]
        
        save_as_dialog = gtk.FileChooserDialog("Save as", self,
                                                gtk.FileChooserAction.SAVE,
                                                ("Cancel", gtk.ResponseType.CANCEL,
                                                "Save", gtk.ResponseType.OK))
        
        save_as_dialog.set_filename(save_path + config_name)
        save_as_dialog.set_do_overwrite_confirmation(True)
        
        response = save_as_dialog.run()

        if response == gtk.ResponseType.OK:
            if app_memory["new_config"]:
                app_memory["new_config"] = False
                
            filename = save_as_dialog.get_filename()
            config_name = filename.split("/")[-1]

            l = len(filename) - len(config_name)
            save_path = filename[0:l]            
            
            app_memory["kconfig_infos"].finish_write_config(save_path + config_name)
            
            app_memory["save_path"] = save_path
            app_memory["config_name"] = config_name

            if app_memory["modified"] == True:
                app_memory["modified"] = False

            self.save_toolbar.set_sensitive(False)
            self.save_menubar.set_sensitive(False)
                            
        save_as_dialog.destroy()

        return response == gtk.ResponseType.OK
        """
        save_path = app_memory["save_path"]
        config_name = app_memory["config_name"]

        save_as_dialog = gtk.FileChooserDialog("Save as", self,
                                        gtk.FileChooserAction.SAVE,
                                        ("Cancel", gtk.ResponseType.CANCEL,
                                        "Save", gtk.ResponseType.OK))

        save_as_dialog.set_filename(save_path + config_name)
        save_as_dialog.set_do_overwrite_confirmation(True)

        response = save_as_dialog.run()

        if response == gtk.ResponseType.OK:
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
        """

    def on_menu1_quit_activate(self, widget):
        exit = True
        if app_memory["modified"]:
            save_btn = "Save"
            label = gtk.Label("Do you want to save the modifications of the " + \
                              "kernel configuration file" + \
                              " «" + app_memory["config_name"] + "» " + \
                              "before to close?")

            if app_memory["new_config"]:
                save_btn += " as"
            
            quit_dialog = gtk.Dialog("Exit", self, 0,
                                     ("Exit whitout save", gtk.ResponseType.NO,
                                     "Cancel", gtk.ResponseType.CANCEL,
                                     save_btn, gtk.ResponseType.YES)) 
            box = quit_dialog.get_content_area()
            box.add(label)
            quit_dialog.show_all()
        
            response = quit_dialog.run()

            if response == gtk.ResponseType.YES:
                if app_memory["new_config"]:
                    is_save = self.on_menu1_save_as_activate(widget)
                    exit = is_save
                else:
                    self.on_menu1_save_activate(widget)
                quit_dialog.destroy()
            elif response == gtk.ResponseType.NO:
                quit_dialog.destroy()
            else:
                quit_dialog.destroy()
                exit = False
                
        if exit:
            self.window.destroy()

        return exit
        """
        if app_memory["modified"]:
            save_btn = "Save"
            label = gtk.Label("Do you want to save the modification of the " +
                              "kernel configuration file" +
                              " «" + app_memory["config_name"] + "» " +
                              "before to close?")

            if app_memory["new_config"]:
                save_btn += " as"

            quit_dialog = gtk.Dialog("Exit", self, 0,
                                    ("Exit whitout save", gtk.ResponseType.NO,
                                     "Cancel", gtk.ResponseType.CANCEL,
                                     save_btn, gtk.ResponseType.YES))
            box = quit_dialog.get_content_area()
            box.add(label)
            quit_dialog.show_all()

            response = quit_dialog.run()

            if response == gtk.ResponseType.YES:
                if app_memory["new_config"]:
                    self.on_menu1_save_as_activate(widget)
                else:
                    self.on_menu1_save_activate(widget)
                quit_dialog.destroy()
                self.on_mainWindow_destroy(widget)
            elif response == gtk.ResponseType.NO:
                quit_dialog.destroy()
                self.on_mainWindow_destroy(widget)
            else:
                quit_dialog.destroy()
        else:
            self.on_mainWindow_destroy(widget)

        #app_memory["kconfig_infos"].write_config(".config")
        #self.window.destroy()
    """
    # TOOLBAR
    def on_new_button_clicked(self, widget):
        self.on_menu1_new_activate(widget)

    def on_save_button_clicked(self, widget):
        self.on_menu1_save_activate(widget)

    def on_save_as_button_clicked(self, widget):
        self.on_menu1_save_as_activate(widget)

    def on_expand_button_clicked(self, widget):
        self.treeview_search.expand_all()

    def on_collapse_button_clicked(self, widget):
        self.treeview_search.collapse_all()


class DialogHelp(gtk.Dialog):
    def __init__(self, parent, text_type):
        gtk.Dialog.__init__(self, "Information", parent, 0, (gtk.STOCK_OK,
                                                            gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = gtk.Label("Erreur")

        if (text_type == "default"):
            label = gtk.Label("DEFAULT -- This is a dialog to \
display additional information ")
        elif (text_type == "load"):
            label = gtk.Label("LOAD -- This is a dialog to \
display additional information ")
        elif (text_type == "error_load_kernel"):
            label = gtk.Label("Error -- You haven't completed the Linux \
Kernel field \n and/or the Architecture field.")
        elif (text_type == "error_load_config"):
            label = gtk.Label("Error --  You haven't completed the \
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
    app_memory["archi_config"] = ""

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

                    if len(sys.argv) == 5:
                        #.config à load
                        app_memory["archi_config"] = sys.argv[4]

    app_memory["open"] = True
    app_memory["to_open"] = "ConfigurationInterface"
    app_memory["save_path"] = app_memory["kernel_path"]
    
    app_memory["kconfig_infos"] = app_core.AppCore()
    while(app_memory["open"]):
        if (app_memory["to_open"] == "ConfigurationInterface"):
            app_memory["config_name"] = ".config"
            app_memory["modified"] = False
            app_memory["new_config"] = True
                        
            ConfigurationInterface(app_memory)
            gtk.main()
        else: #elif (app_memory["to_open"] == "OptionsInterface"):
            OptionsInterface(app_memory)
            gtk.main()


"""
Faire une grosse classe MAIN qui ouvre les fenetres
Qui récupère les valeurs de retours de fenetre pour en ouvrir d'autres
Et cette classe stockera les informations nécessaire a l'application
(options, option courante, ...)
"""
