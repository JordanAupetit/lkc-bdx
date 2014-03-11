#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

#(’°O°)’

from gi.repository import Gtk

import os
import sys

sys.path.append("modules/")
import utility
import search
sys.path.append("parser/kconfiglib/")
import kconfiglib


#   ==========================
#   ==== TODO 
#   ==========================
#
#   - Enlever les boutons radios lorsqu'ils n'y a pas tous les choix 
#   (que y or n)
#
#   - Faire la page de démarrage de la page des options
#
#   - Afficher les options sous forme de liste à cocher 
#   pour l'onglet Search
#
#   - Générer une config avec defconfig
#
#   - Générer une config avec load config
#
#   - Gérer le choix d'une architecture
#
#   - Générer un .config avec la touche "Finish" === OK
#
#   - Voir si on peut améliorer le chargement du kconfig avec un Thread
#
#   - Afficher une POP-UP si on clique sur Next pour dire que 
#   l'architecture n'est pas selectionné / ou pas de kernel selectionné
#
#   - On ne traite ici QUE l'affichage des symboles et pas des menus, 
#   choice or comment
#
#
#
#
#



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
        self.combo_text_archi = self.interface.get_object("combo_text_archi")

        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            app_memory["open"] = False
        #else:
        #    self.toClose = True

        Gtk.main_quit()


    def on_btn_choose_kernel_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.input_choose_kernel.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_btn_choose_config_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.input_choose_config.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


    def on_btn_help_default_clicked(self, widget):
        dialog = DialogHelp(self.window, "default")
        dialog.run()
        dialog.destroy()

    def on_btn_help_empty_clicked(self, widget):
        dialog = DialogHelp(self.window, "empty")
        dialog.run()
        dialog.destroy()

    def on_btn_help_hardware_clicked(self, widget):
        dialog = DialogHelp(self.window, "hardware")
        dialog.run()
        dialog.destroy()

    def on_btn_help_load_clicked(self, widget):
        dialog = DialogHelp(self.window, "load")
        dialog.run()
        dialog.destroy()

    def on_btn_stop_clicked(self, widget):
        print("Nothing")

    def on_btn_next_clicked(self, widget):
        
        path = self.input_choose_kernel.get_text()

        # Ajout d'un "/" a la fin du chemin s'il y est pas
        if (path[len(path) - 1] != "/"):
            path += "/"

        #path = "/net/travail/jaupetit/linux-3.13.5/"

        # initialisation de l'environement
        arch = "x86_64"
        utility.init_environ(path, arch)

        kconfig_infos = kconfiglib.Config(filename=path+"Kconfig",
            base_dir=path, print_warnings=False)



        r = search.search(kconfig_infos, "e1000")
        print "-------------------"
        print_items(r, 4)
        print "-------------------"
        
        print "Verification de l'architecture"
        print kconfig_infos.get_srcarch()
        print kconfig_infos.get_arch() + "\n"

        print "Vérification du chemin et de la version du noyau"
        print kconfig_infos.get_srctree()
        print os.environ.get("KERNELVERSION") + "\n"

        #kconfig_infos.load_config("/net/travail/jaupetit/linux-3.13.5/.config")
        app_memory["kconfig_infos"] = kconfig_infos


        self.toClose = False
        app_memory["to_open"] = "OptionsInterface"
        self.window.destroy()


    def on_btn_exit_clicked(self, widget):
        print("Btn EXIT clicked")
        self.window.destroy()


class OptionsInterface():
    def __init__(self, app_memory):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('interface/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory
        self.current_option = -1
        self.top_level_items = app_memory["kconfig_infos"].get_top_level_items()
        self.items = self.get_all_items(self.top_level_items, [])

        #print len(self.items)

        self.label_title_option = \
            self.interface.get_object("label_title_option")
        self.radio_yes = self.interface.get_object("radio_yes")
        self.radio_module = self.interface.get_object("radio_module")
        self.radio_no = self.interface.get_object("radio_no")
        self.label_description_option = \
            self.interface.get_object("label_description_option")
        self.btn_next = self.interface.get_object("btn_next")
        self.input_search = self.interface.get_object("input_search")
        self.list_options = self.interface.get_object("list_options")


        #current_item = app_memory["kconfig_infos"].get_symbol('RFKILL')
        #print "Name => " + current_item.get_name(), " | ", current_item.is_modifiable(), " | ", current_item.get_visibility(), " | ", "Value => " + current_item.get_value(), current_item.get_assignable_values()

        #print_items(app_memory["kconfig_infos"].get_top_level_items(), 0)
        # /net/travail/jaupetit/linux-3.13.5/   


        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            app_memory["open"] = False

        Gtk.main_quit()

    def on_btn_keyword_clicked(self, widget):
        print("Nothing")

    def on_btn_resolve_clicked(self, widget):
        print("Nothing")

    def on_btn_back_clicked(self, widget):
        print("Nothing")

    def on_btn_next_clicked(self, widget):
        self.current_option += 1
        current_item = self.items[self.current_option]

        while(current_item.is_symbol() == False):
            self.current_option += 1
            current_item = self.items[self.current_option]

            if current_item.is_menu():
                print("Menu")
            if current_item.is_choice():
                print("Choice")
            if current_item.is_comment():
                print("Comment")
        
        self.change_option()

    def on_btn_search_clicked(self, widget):
        self.list_options.set_text(self.input_search.get_text())

    def on_btn_finish_clicked(self, widget):
        app_memory["kconfig_infos"].write_config(".config")
        self.window.destroy()

    def change_option(self):

        current_item = self.items[self.current_option]
        self.label_title_option \
            .set_text("Do you want " + current_item.get_name() + \
            " option enabled ?")

        help_text = current_item.get_help()
        value = current_item.get_value()
        assignable_values = current_item.get_assignable_values()

        if (help_text != None):
            self.label_description_option.set_text(help_text)
        else:
            self.label_description_option.set_text("No help available.")


        #print "Name => " + current_item.get_name(), " | ", current_item.is_modifiable(), " | ", current_item.get_visibility(), " | ", "Value => " + current_item.get_value(), assignable_values

        if (value == "y"):
            self.radio_yes.set_active(True)
        if (value == "m"):
            self.radio_module.set_active(True)
        if (value == "n"):
            self.radio_no.set_active(True)

        self.radio_yes.set_sensitive(False)
        self.radio_module.set_sensitive(False)
        self.radio_no.set_sensitive(False)

        if (current_item.get_type() == kconfiglib.BOOL):
            self.radio_yes.set_sensitive(True)
            self.radio_no.set_sensitive(True)
        elif (current_item.get_type() == kconfiglib.TRISTATE):
            self.radio_yes.set_sensitive(True)
            self.radio_module.set_sensitive(True)
            self.radio_no.set_sensitive(True)

        # if ("y" not in assignable_values):
        #     self.radio_yes.set_sensitive(False)
        # if ("m" not in assignable_values):
        #     self.radio_module.set_sensitive(False)
        # if ("n" not in assignable_values):
        #     self.radio_no.set_sensitive(False)

    def get_all_items(self, items, list):
        for item in items:
            if item.is_symbol():
                list.append(item)
            elif item.is_menu():
                for i in item.get_items(True):
                    list.append(i)
            elif item.is_choice():
                list.append([])
            elif item.is_comment():
                list.append([])

        return list


class DialogHelp(Gtk.Dialog):
    def __init__(self, parent, text_type):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Erreur")

        if (text_type  == "default"):
            label = Gtk.Label("DEFAULT -- This is a dialog to \
                display additional information ")
        elif (text_type  == "empty"):
            label = Gtk.Label("EMPTY -- This is a dialog to \
                display additional information ")
        elif (text_type  == "hardware"):
            label = Gtk.Label("HARDWARE -- This is a dialog \
                to display additional information ")
        elif (text_type  == "load"):
            label = Gtk.Label("LOAD -- This is a dialog to \
                display additional information ")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


# DEBUG <<<<
def print_with_indent(s, indent):
    print (" " * indent) + s

# DEBUG <<<<
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

# def main():
#     """ Main function """
#     os.environ["ARCH"] = "x86_64"
#     utility.match("x86_64")

if __name__ == "__main__":
    
    app_memory = {}
    app_memory["open"] = True
    app_memory["to_open"] = "ConfigurationInterface"

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
