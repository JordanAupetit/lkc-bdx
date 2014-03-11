#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

from gi.repository import Gtk

import os
import sys

sys.path.append("modules/")
import utility

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
#   - Afficher les options sous forme de liste à cocher pour l'onglet Search
#
#   - Générer une config avec defconfig
#
#   - Générer une config avec load config
#
#   - Gérer le choix d'une architecture
#
#   - Générer un .config avec la touche "Finish"
#
#   - Voir si on peut améliorer le chargement du kconfig avec un Thread
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
        if(self.toClose):
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
        if(path[len(path) - 1] != "/"):
            path += "/"

        #path = "/net/travail/jaupetit/linux-3.13.5/"

        # initialisation de l'environement
        arch = "x86_64"
        utility.init(path, arch)

        kconfig_infos = kconfiglib.Config(filename=path+"Kconfig",
            base_dir=path, print_warnings=False)

        print "Verification de l'architecture"
        print kconfig_infos.get_srcarch()
        print kconfig_infos.get_arch() + "\n"

        print "Vérification du chemin et de la version du noyau"
        print kconfig_infos.get_srctree()
        print os.environ.get("KERNELVERSION") + "\n"


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
        self.items = app_memory["kconfig_infos"].get_top_level_items()

        self.label_title_option = \
            self.interface.get_object("label_title_option")
        self.radio_yes = self.interface.get_object("radio_yes")
        self.radio_module = self.interface.get_object("radio_module")
        self.radio_no = self.interface.get_object("radio_no")
        self.label_description_option = \
            self.interface.get_object("label_description_option")
        self.btn_next = self.interface.get_object("btn_next")

        #print_items(app_memory["kconfig_infos"].get_top_level_items(), 0)
        # /net/travail/jaupetit/linux-3.13.5/


        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if(self.toClose):
            app_memory["open"] = False

        Gtk.main_quit()

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

    def change_option(self):

        current_item = self.items[self.current_option]
        self.label_title_option \
            .set_text("Do you want " + \
            current_item.get_name() + \
            " option enabled ?")

        help_text = current_item.get_help()
        value = current_item.get_value()

        if(help_text != None):
            self.label_description_option.set_text(help_text)
        else:
            self.label_description_option.set_text("No help available.")

        print("Value => " + current_item.get_value())

        if(value == "y"):
            self.radio_yes.set_active(True)
        if(value == "m"):
            self.radio_module.set_active(True)
        if(value == "n"):
            self.radio_no.set_active(True)


class DialogHelp(Gtk.Dialog):
    def __init__(self, parent, text_type):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Erreur")

        if(text_type  == "default"):
            label = Gtk.Label("DEFAULT -- This is a dialog to \
                display additional information ")
        elif(text_type  == "empty"):
            label = Gtk.Label("EMPTY -- This is a dialog to \
                display additional information ")
        elif(text_type  == "hardware"):
            label = Gtk.Label("HARDWARE -- This is a dialog \
                to display additional information ")
        elif(text_type  == "load"):
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
        if(app_memory["to_open"] == "ConfigurationInterface"):
            ConfigurationInterface(app_memory)
            Gtk.main()
        elif(app_memory["to_open"] == "OptionsInterface"):
            OptionsInterface(app_memory)
            Gtk.main()


"""
Faire une grosse classe MAIN qui ouvre les fenetres
Qui récupère les valeurs de retours de fenetre pour en ouvrir d'autres
Et cette classe stockera les informations nécessaire a l'application 
(options, option courante, ...)
"""
