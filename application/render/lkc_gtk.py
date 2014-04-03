#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import Gdk as gdk

import sys
import os
import threading

sys.path.append("../core/")
import core

sys.path.append("../sync/")
import callback

# Init callback's thread
gobject.threads_init()

# Fetch all glades interfaces
script_path = os.path.dirname(os.path.realpath(__file__)) + "/interface"


class ConfigurationInterface(gtk.Window):
    def __init__(self, app_memory):
        self.interface = gtk.Builder()
        self.interface.add_from_file(script_path+'/chooseConfiguration.glade')
        self.window = self.interface.get_object('mainWindow')

        x = self.interface

        self.input_choose_kernel = x.get_object('input_choose_kernel')
        self.btn_choose_kernel = x.get_object('btn_choose_kernel')
        self.combo_text_archi_folder = x.get_object('combo_text_archi_folder')
        self.combo_text_archi_defconfig = \
            x.get_object('combo_text_archi_defconfig')
        self.radio_default = x.get_object('radio_default')
        self.btn_help_default = x.get_object('btn_help_default')
        self.radio_load = x.get_object('radio_load')
        self.btn_help_load = x.get_object('btn_help_load')
        self.progress_bar = x.get_object('progressbar')
        self.btn_stop = x.get_object('btn_stop')
        self.btn_next = x.get_object('btn_next')

        self.list = [self.input_choose_kernel,
                     self.btn_choose_kernel,
                     self.combo_text_archi_folder,
                     self.combo_text_archi_defconfig,
                     self.radio_default,
                     self.btn_help_default,
                     self.radio_load,
                     self.btn_help_load,
                     self.btn_next]

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

        self.cb = None

        if self.app_memory["kernel_path"] != "":
            self.input_choose_kernel.set_text(self.app_memory["kernel_path"])

    def on_mainWindow_destroy(self, widget):
        if (self.toClose):
            self.app_memory["open"] = False

        if self.cb is not None:
            self.cb.stop()
        gtk.main_quit()

    def on_btn_stop_clicked(self, widget):
        if self.cb is not None:
            self.cb.stop()
            self.window.set_focus(None)
            self.window.set_focus(self.btn_next)

    def on_btn_choose_kernel_clicked(self, widget):
        dialog = gtk.FileChooserDialog("Please choose a folder", self.window,
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
        # res[0][X][0] contient la liste des architectures (X)
        for arch in res[0]:
            self.combo_text_archi_folder.append_text(arch[0])
            i += 1
            if arch[0] == self.app_memory["archi_folder"]:
                i_archi_folder = i - 1

        self.combo_text_archi_folder.set_active(i_archi_folder)

    def on_combo_text_archi_folder_changed(self, widget):
        arch_active = self.combo_text_archi_folder.get_active_text()

        if arch_active is not None:
            # tmp contient la liste des architectures compatibles
            # avec le noyau linux
            tmp = self.app_memory["kconfig_infos"].archs
            self.app_memory["archi_folder"] = arch_active
            i_defconfig = 0
            j = 0
            for arch in tmp:
                if arch_active == arch[0]:
                    self.combo_text_archi_defconfig.set_sensitive(True)
                    self.combo_text_archi_defconfig.remove_all()
                    if type(arch[1]) is list:
                        for i in arch[1]:
                            self.combo_text_archi_defconfig.append_text(i)
                            j += 1
                            if i == self.app_memory["archi_src"]:
                                i_defconfig = j - 1
                        break
                    else:
                        self.combo_text_archi_defconfig.append_text(arch[1])
                        i_defconfig = 0
                        break
            self.combo_text_archi_defconfig.set_active(i_defconfig)

    def on_combo_text_archi_defconfig_changed(self, widget):
        arch_active = widget.get_active_text()
        if arch_active is not None:
            self.app_memory["archi_src"] = arch_active

    def on_btn_choose_config_clicked(self, widget):
        dialog = gtk.FileChooserDialog("Please choose a file",
                                       self.window,
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

    def callback_set_progress(self, progress):
        self.progress_bar.set_fraction(progress)
        self.progress_bar.set_text(str(progress*100)+"%")

    def callback_set_finished(self):
        self.progress_bar.set_fraction(1.0)
        self.progress_bar.set_text("100%")
        self.toClose = False
        self.app_memory["to_open"] = "OptionsInterface"
        self.window.destroy()

    def on_callback_reset(self):
        for i in self.list:
            i.set_sensitive(True)
        self.progress_bar.set_text("0%")
        self.progress_bar.set_fraction(0)

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

        if self.radio_state == "default":
            print "Configuration by default"
            load_config = ""
        elif self.radio_state == "load":
            print "Configuration by load"
            load_config = self.input_choose_config.get_text()
            if not self.app_memory["kconfig_infos"]\
                       .is_config_file_correct(load_config):
                label = gtk.Label("Please choose a correct "
                                  ".config file to load")
                bad_conf = gtk.Dialog("Bad .config", self, 0,
                                      ("Ok", gtk.ResponseType.YES))
                box = bad_conf.get_content_area()
                box.add(label)
                bad_conf.show_all()
                response = bad_conf.run()
                if response == gtk.ResponseType.YES:
                    bad_conf.destroy()
                return

        for i in self.list:
            i.set_sensitive(False)

        def create_mem_config():
            self.cb = callback.Callback(self.callback_set_progress)
            self.app_memory["kconfig_infos"].init_memory(path,
                                                         arch,
                                                         srcarch,
                                                         load_config,
                                                         self.cb)
            if self.cb.stopped is True:
                gobject.idle_add(self.on_callback_reset)
                return
            gobject.idle_add(self.callback_set_finished)

        thread = threading.Thread(target=create_mem_config)
        thread.start()
        self.window.set_focus(self.btn_stop)

    def on_radio_default_clicked(self, widget):
        self.radio_state = "default"
        self.input_choose_config.set_sensitive(False)
        self.btn_choose_config.set_sensitive(False)

    def on_radio_load_clicked(self, widget):
        self.radio_state = "load"
        if self.app_memory["config_load"] != "":
            self.input_choose_config.set_text(self.app_memory["config_load"])
        self.input_choose_config.set_sensitive(True)
        self.btn_choose_config.set_sensitive(True)

    def on_btn_exit_clicked(self, widget):
        self.window.destroy()


class OptionsInterface(gtk.Window):
    def __init__(self, app_memory):
        self.interface = gtk.Builder()
        self.interface.add_from_file(script_path+'/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory

        #self.window.set_title("Linux Kernel Configuration - Architecture : " +
        #                      app_memory["kconfig_infos"].get_srcarch())

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
        self.label_current_menu = self.interface\
                                      .get_object("label_current_menu")
        self.notebook = self.interface.get_object("notebook2")

        self.save_toolbar = self.interface.get_object('save_button')
        self.save_menubar = self.interface.get_object('menu1_save')

        self.menu3_name = self.interface.get_object('menu3_name')
        self.menu3_description = \
            self.interface.get_object('menu3_description')
        self.menu3_help = self.interface.get_object('menu3_help')

        self.btn_back.set_sensitive(False)

        self._add_tree_view()
        # Init all trees options (section and conflicts)
        self._get_tree_option()
        self._add_section_tree()
        self._add_conflicts_tree()

        self.interface.connect_signals(self)

    def on_mainWindow_delete_event(self, widget, data):
        self.on_menu1_quit_activate(widget)
        return True

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            self.app_memory["open"] = False
        gtk.main_quit()

    def on_btn_back_clicked(self, widget):
        tmp = self.app_memory["kconfig_infos"].goto_back_opt()
        if tmp is False:
            self.btn_back.set_sensitive(False)
        elif tmp is True:
            self.btn_back.set_sensitive(True)
        self.btn_next.set_sensitive(True)
        self._change_option()

    def on_btn_next_clicked(self, widget):
        goto_next = self.app_memory["kconfig_infos"].goto_next_opt()

        if goto_next is False:
            self.btn_next.set_sensitive(False)

        if not self.app_memory["modified"]:
            self.app_memory["modified"] = True

        self.radio_yes.set_visible(True)
        self.radio_module.set_visible(True)
        self.radio_no.set_visible(True)

        if self.app_memory["kconfig_infos"].goto_back_is_possible() is True:
            self.btn_back.set_sensitive(True)

        self._change_option()

    def _set_value(self):
        changed = False
        if self.app_memory["kconfig_infos"].is_current_opt_symbol():
            value = self.app_memory["kconfig_infos"].get_current_opt_value()
            if self.radio_yes.get_active() and value != "y":
                value = "y"
                changed = True
            elif self.radio_module.get_active() and value != "m":
                value = "m"
                changed = True
            elif self.radio_no.get_active() and value != "n":
                value = "n"
                changed = True
        elif self.app_memory["kconfig_infos"].is_current_opt_choice():
            symbol_selected = self.combo_choice.get_active_text()
            symbol_name = ""

            if symbol_selected is not None:
                symbol_name = self.app_memory["kconfig_infos"]\
                                  .get_name_in_str(symbol_selected)
            if symbol_name == "No choice are selected":
                value = "N"
                changed = True
            else:
                value = symbol_name
                changed = True

        if changed:
            self.app_memory["kconfig_infos"].set_current_opt_value(value)
            print "Value setted ! => " + str(value)

            if not self.app_memory["modified"]:
                self.app_memory["modified"] = True

            self.save_toolbar.set_sensitive(True)
            self.save_menubar.set_sensitive(True)

    def on_radio_yes_clicked(self, widget):
        self._set_value()

    def on_radio_module_clicked(self, widget):
        self._set_value()

    def on_radio_no_clicked(self, widget):
        self._set_value()

    def _change_interface_conflit(self):
        self.move_cursor_conflicts_allowed = False
        self.treestore_conflicts.clear()
        self.move_cursor_conflicts_allowed = True

        self.radio_yes.set_sensitive(True)
        self.radio_no.set_sensitive(True)
        self.radio_module.set_sensitive(True)

        if self.app_memory["kconfig_infos"].is_current_opt_symbol():
            value = self.app_memory["kconfig_infos"].get_current_opt_value()
            modifiable = self.app_memory["kconfig_infos"]\
                             .is_current_opt_modifiable()

            if value == "y" and not modifiable:
                self.radio_no.set_sensitive(False)
                self.radio_module.set_sensitive(False)
            if value == "n" and not modifiable:
                self.radio_yes.set_sensitive(False)
                self.radio_module.set_sensitive(False)
            if value == "m" and not modifiable:
                self.radio_no.set_sensitive(False)

        list_conflicts = self.app_memory["kconfig_infos"]\
            .get_current_opt_conflict()

        if list_conflicts != []:
            if self.app_memory["kconfig_infos"].is_current_opt_choice():
                sym_selected = self.combo_choice.get_active_text()
                choice_symbol_name = ""
                if sym_selected is not None:
                    choice_symbol_name = self.app_memory["kconfig_infos"]\
                                             .get_name_in_str(sym_selected)
                for i in list_conflicts:
                    if choice_symbol_name == i[0]:
                        list_conflicts = i
                        break

            # Always true
            if len(list_conflicts) == 2:
                if list_conflicts[1] != []:
                    if len(list_conflicts[1]) == 1:
                        # One conflict
                        self.treestore_conflicts.append(None,
                                                        list_conflicts[1])
                    else:
                        for i in list_conflicts[1]:
                            if i != []:
                                if type(i) is list and len(i) == 1:
                                    self.treestore_conflicts.append(None, i)
                                else:
                                    self.treestore_conflicts.append(None, [i])

                    # Prevent to change option automatically
                    self.move_cursor_conflicts_allowed = False
                    self.treeview_conflicts.set_cursor(0)
                    self.move_cursor_conflicts_allowed = True

                else:
                    # No conflicts
                    self.treestore_conflicts\
                        .append(None, ["No conflicts found.\n"
                                       "Please try looking in the bottom right"
                                       " blocks\nto find the problem.\n"
                                       "It is also possible that the "
                                       "option is not editable."])

                    # Prevent to change option automatically
                    self.move_cursor_conflicts_allowed = False
                    self.treeview_conflicts.set_cursor(0)
                    self.move_cursor_conflicts_allowed = True

    def on_combo_choice_changed(self, widget):
        active_text = self.combo_choice.get_active_text()
        choice_symbol_name = ""
        if active_text is not None:
            choice_symbol_name = self.app_memory["kconfig_infos"]\
                                     .get_name_in_str(active_text)

        res = self.app_memory["kconfig_infos"]\
                  .is_selection_opt_choice_possible(choice_symbol_name)

        print active_text
        print choice_symbol_name
        print "666 => " + str(res)

        if res is True:
            self._set_value()
        self._change_interface_conflit()

    def on_btn_search_clicked(self, widget):
        if self.input_search.get_text() != "":
            self.search_options()
        else:
            self._get_tree_option()

    def on_input_search_activate(self, widget):
        self.search_options()

    def on_btn_clean_search_clicked(self, widget):
        self._get_tree_option()
        self.input_search.set_text("")

    def search_options(self):
        pattern = self.input_search.get_text()

        n = self.menu3_name.get_active()
        d = self.menu3_description.get_active()
        h = self.menu3_help.get_active()

        result_search = self.app_memory["kconfig_infos"]\
                            .search_options_from_pattern(pattern, n, d, h)

        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        title = "Matching option"
        if len(result_search) > 1:
            title += "s"

        self._get_tree_option_rec(result_search, None)

        title += " : " + str(len(self.treestore_search))
        self.change_title_column_treeview(title, 0)

    def _get_tree_option(self):
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
                if self.app_memory["kconfig_infos"].is_valid_symbol(i[0]):
                    if self.app_memory["kconfig_infos"].is_choice_symbol(i[0]):
                        i[0] = self.app_memory["kconfig_infos"]\
                                   .get_prompt_parent_choice(i)
                    self.treestore_search.append(parent, [i[0]])
                elif len(i) == 2:
                    menu = self.treestore_search.append(parent, [i[0]])
                    self._get_tree_option_rec(i[1], menu)
            else:
                if self.app_memory["kconfig_infos"].is_valid_symbol(i):
                    if self.app_memory["kconfig_infos"].is_choice_symbol(i):
                        i = self.app_memory["kconfig_infos"]\
                                .get_prompt_parent_choice(i)

                    self.treestore_search.append(parent, [i])

        # Prevent to change option automatically
        self.move_cursor_search_allowed = False
        self.treeview_search.set_cursor(0)
        self.move_cursor_search_allowed = True

    def on_btn_finish_clicked(self, widget):
        self.on_menu1_quit_activate(widget)

    def _change_option(self):
        self._change_interface_conflit()

        help_text = self.app_memory["kconfig_infos"].get_current_opt_help()
        condition_test = "".join(self.app_memory["kconfig_infos"]
                                     .get_current_opt_conditions())

        description_text = help_text
        description_text = help_text + "\n\n" + condition_test

        self.label_description_option.set_text(description_text)

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
            text += "Do you want to change"\
                    " the selected option of this choice ? \n"

            if len(prompt) > 0:
                text += prompt[0]

            self.label_title_option.set_text(text)

            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)

            self.combo_choice.set_visible(True)
            self.combo_choice.remove_all()
            self.combo_choice.append_text("«No choice are selected»")
            self.combo_choice.set_active(0)

            combo_setted = False
            index_combo = 1

            symbols_name = self.app_memory["kconfig_infos"]\
                               .get_current_choice_symbols_name()

            tmp = ""
            for item, value, modifiable in symbols_name:
                tmp = "«" + item + "»"
                if not modifiable:
                    tmp += " -- Not settable"
                self.combo_choice.append_text(tmp)
                if value == "y":
                    self.combo_choice.set_active(index_combo)
                    combo_setted = True

                index_combo += 1

            if combo_setted:
                self.combo_choice.remove(0)

    def change_title_column_treeview(self, title, id_column):
        column = self.treeview_search.get_column(id_column)
        column.set_title(title)

    def _add_tree_view(self, title="List of options"):
        self.treeview_search.set_enable_tree_lines(True)
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn(title, renderer_text, text=0)
        self.treeview_search.append_column(column_text)
        self.treeview_search.set_enable_search(False)
        self.treeview_search.connect("cursor-changed",
                                     self.on_cursor_treeview_search_changed)

        scrolledwindow_search = self.interface\
                                    .get_object("scrolledwindow_search")
        scrolledwindow_search.add(self.treeview_search)
        scrolledwindow_search.show_all()

    def _add_section_tree(self):
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Sections", renderer_text, text=0)
        self.treeview_section.append_column(column_text)
        self.treeview_section.set_enable_search(False)
        self.treeview_section.connect("cursor-changed",
                                      self.on_cursor_treeview_section_changed)

        scrolledwindow_section = self.interface\
                                     .get_object("scrolledwindow_section")
        scrolledwindow_section.add(self.treeview_section)

        self.treestore_section\
            .append(None,
                    ["General options (options without menu)"])

        top_menus = self.app_memory["kconfig_infos"].get_all_topmenus_name()
        for m in top_menus:
            self.treestore_section.append(None, [m])

        scrolledwindow_section.show_all()

    def _add_conflicts_tree(self):
        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Conflicts", renderer_text, text=0)
        self.treeview_conflicts.append_column(column_text)
        self.treeview_conflicts.set_enable_search(False)
        self.treeview_conflicts\
            .connect("cursor-changed",
                     self.on_cursor_treeview_conflicts_changed)

        scrolledwindow_conflicts = self.interface\
                                       .get_object("scrolledwindow_conflicts")
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

                if self.app_memory["kconfig_infos"].goto_back_is_possible():
                    self.btn_back.set_sensitive(True)

                if res == 0:
                    self.btn_next.set_sensitive(True)
                    self._change_option()

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
                    menus = self.app_memory["kconfig_infos"]\
                                .get_all_topmenus_name()
                    for menu in menus:
                        if menu_title == menu:
                            find = True
                            break
                        cpt += 1
                if find:
                    first_option_index_menu = 0

                    if cpt == -1:
                        first_option_index_menu = self\
                            .app_memory["kconfig_infos"]\
                            .get_first_option_menu()
                    else:
                        first_option_index_menu = self\
                            .app_memory["kconfig_infos"]\
                            .get_id_option_menu(cpt)

                    self.app_memory["kconfig_infos"]\
                        .goto_opt(first_option_index_menu)

                    if self.app_memory["kconfig_infos"]\
                           .goto_back_is_possible():
                        self.btn_back.set_sensitive(True)

                    self.btn_next.set_sensitive(True)
                    self._change_option()

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
                    self.btn_next.set_sensitive(True)
                    self._change_option()

                    if self.app_memory["kconfig_infos"]\
                           .goto_back_is_possible():
                        self.btn_back.set_sensitive(True)

                    self.move_cursor_conflicts_allowed = False
                    self.treestore_conflicts.clear()
                    self.move_cursor_conflicts_allowed = True

    # MENUBAR
    def on_menu1_new_activate(self, widget):
        print "new"
        self.toClose = False
        if self.on_menu1_quit_activate(widget):
            self.window.destroy()
            self.app_memory["to_open"] = "ConfigurationInterface"
            gtk.main_quit()

    def on_menu1_save_activate(self, widget):
        if self.app_memory["new_config"]:
            self.on_menu1_save_as_activate(widget)
        else:
            save_path = self.app_memory["save_path"]
            config_name = self.app_memory["config_name"]

            self.app_memory["kconfig_infos"]\
                .finish_write_config(save_path + config_name)

            if self.app_memory["modified"] is True:
                self.app_memory["modified"] = False
            self.save_toolbar.set_sensitive(False)
            self.save_menubar.set_sensitive(False)

    def on_menu1_save_as_activate(self, widget):
        save_path = self.app_memory["save_path"]
        config_name = self.app_memory["config_name"]

        save_as_dialog = gtk.FileChooserDialog("Save as", self.window,
                                               gtk.FileChooserAction.SAVE,
                                               ("Cancel", gtk.ResponseType
                                                             .CANCEL,
                                                "Save", gtk.ResponseType.OK))

        save_as_dialog.set_filename(save_path + config_name)
        save_as_dialog.set_do_overwrite_confirmation(True)

        response = save_as_dialog.run()

        if response == gtk.ResponseType.OK:
            if self.app_memory["new_config"]:
                self.app_memory["new_config"] = False

            filename = save_as_dialog.get_filename()
            config_name = filename.split("/")[-1]

            l = len(filename) - len(config_name)
            save_path = filename[0:l]

            self.app_memory["kconfig_infos"]\
                .finish_write_config(save_path + config_name)

            self.app_memory["save_path"] = save_path
            self.app_memory["config_name"] = config_name

            if self.app_memory["modified"] is True:
                self.app_memory["modified"] = False

            self.save_toolbar.set_sensitive(False)
            self.save_menubar.set_sensitive(False)

        save_as_dialog.destroy()

        return response == gtk.ResponseType.OK

    def on_menu1_quit_activate(self, widget):
        exit = True
        if self.app_memory["modified"]:
            save_btn = "Save"
            label = gtk.Label("Do you want to save the modifications of the "
                              "kernel configuration file"
                              " «" + self.app_memory["config_name"] + "» "
                              "before to close?")

            if self.app_memory["new_config"]:
                save_btn += " as"

            quit_dialog = gtk.Dialog("Exit", self.window, gtk.DialogFlags.MODAL,
                                     ("Exit whitout save", gtk.ResponseType.NO,
                                      "Cancel", gtk.ResponseType.CANCEL,
                                      save_btn, gtk.ResponseType.YES))
            box = quit_dialog.get_content_area()
            box.add(label)
            quit_dialog.show_all()

            response = quit_dialog.run()

            if response == gtk.ResponseType.YES:
                if self.app_memory["new_config"]:
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

    def on_menu2_introduction_activate(self, widget):
        dialog = DialogHelp(self.window, "introduction")
        dialog.run()
        dialog.destroy()


    def on_menu2_about_activate(self, widget):
        # http://www.pygtk.org/pygtk2reference/class-gtkaboutdialog.html#constructor-gtkaboutdialog
        d = gtk.AboutDialog()
        
        #d.set_gravity(gdk.GRAVITY_CENTER)

        d.set_name("Linux Configuration Tool")
        d.set_program_name("Linux Configuration Tool")
        d.set_version("1.0")
        d.set_copyright("copyright")
        d.set_comments("comment")
        d.set_license("GPL3")
        d.set_authors("c'est nous qu'on l'a fait")

        d.run()
        d.destroy()

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

    def on_help_button_clicked(self, widget):
        self.on_menu2_introduction_activate(widget)


class DialogHelp(gtk.MessageDialog):
    def __init__(self, parent, text_type):
        primary_text = "Erreur"
        secondary_text = ""
        message_type = gtk.MessageType.ERROR

        if text_type == "default":
            primary_text = "Default"
            secondary_text = "Create a default configutation file based\n\
on the selectionned architecture."
            message_type = gtk.MessageType.INFO

        elif text_type == "load":
            primary_text = "Open"
            secondary_text = "Open and load an existing configuration file."
            message_type = gtk.MessageType.INFO

        elif text_type == "error_load_kernel":
            primary_text = "Missing Linux kernel"
            secondary_text = "You haven't completed the Linux Kernel field."

        elif text_type == "error_load_config":
            primary_text = "Missing Linux configuration"
            secondary_text = "You have not choose a Linux configuration file."

        elif text_type == "introduction":
            primary_text = "Welcome to the linux configuration tool !"
            secondary_text = "For each option, you can change its value if there is no \
conflict. You can see the existing conflicts in the associated tab.\n\n"
            secondary_text += "You can navigate between the options by pressing the Next \
button to go to the option that follows.\n"
            secondary_text += "You can click Back to return to previous options.\n\n"
            secondary_text += "There are also three tabs:\n"
            secondary_text += "\t┌ The Section tab contains options organized by menus\n"
            secondary_text += "\t├ The Search tab shows all the options tree or options \
corresponding to a \n\t│ search. You can change the parameters of the research to refine the results.\n"
            secondary_text += "\t└ The Conflicts tab shows the current conflicts option \
for quick access.\n"
            message_type = gtk.MessageType.INFO

        gtk.MessageDialog.__init__(self, parent, gtk.DialogFlags.MODAL,
                                   message_type, gtk.ButtonsType.NONE,
                                   primary_text)

        self.add_button("Ok", gtk.ResponseType.OK)
        self.format_secondary_text(secondary_text)
        self.show_all()


def usage():
    """ Print script's usage from cli """
    print "---- USAGE Function ---- "
    print "./app_render_gtk.py kernel_path src_arch arch config_to_load"
    print "Example : ./app_render_gtk.py ~/home/user/linux-3.13"\
          " x86 x86_64 ~/home/user/.config"
    print "All arguments must be in that order (partially if you want to)"
    print "---- ---- ---- ---- ----"

def main():
    app_memory = {}
    app_memory["kernel_path"] = ""
    app_memory["archi_folder"] = "x86"
    app_memory["archi_src"] = "x86_64"
    app_memory["config_load"] = ""

    usage()
    if len(sys.argv) >= 2:
        app_memory["kernel_path"] = sys.argv[1]
        if len(sys.argv) >= 3:
            app_memory["archi_folder"] = sys.argv[2]
            if len(sys.argv) >= 4:
                app_memory["archi_src"] = sys.argv[3]
                if len(sys.argv) >= 5:
                    app_memory["config_load"] = sys.argv[4]

    app_memory["open"] = True
    app_memory["to_open"] = "ConfigurationInterface"
    app_memory["save_path"] = app_memory["kernel_path"]

    app_memory["kconfig_infos"] = core.AppCore()
    while(app_memory["open"]):
        if (app_memory["to_open"] == "ConfigurationInterface"):
            app_memory["config_name"] = ".config"
            app_memory["modified"] = False
            app_memory["new_config"] = True

            ConfigurationInterface(app_memory)
            gtk.main()
        else:
            OptionsInterface(app_memory)
            gtk.main()

if __name__ == '__main__':
    main()
