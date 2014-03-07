#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

from gi.repository import Gtk

import os
import sys

sys.path.append("../pythonUtilitaire")
import utility

sys.path.append("../Kconfiglib")
import kconfiglib



class ConfigurationInterface():
    def __init__(self):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('chooseConfiguration_V2.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True

        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if(self.toClose):
            Gtk.main_quit()
        else:
            self.toClose = True

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
        # Apply configuration <<<
        # print("Configuration loaded")
        # OptionsInterface()

        # self.toClose = False
        # self.window.destroy()

        print("Testing !")

    def on_btn_exit_clicked(self, widget):
        print("Btn EXIT clicked")
        self.window.destroy()


class OptionsInterface():
    def __init__(self):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True

        self.interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if(self.toClose):
            Gtk.main_quit()
        else:
            self.toClose = True


class DialogHelp(Gtk.Dialog):
    def __init__(self, parent, text_type):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Erreur")

        if(text_type  == "default"):
            label = Gtk.Label("DEFAULT -- This is a dialog to display additional information ")
        elif(text_type  == "empty"):
            label = Gtk.Label("EMPTY -- This is a dialog to display additional information ")
        elif(text_type  == "hardware"):
            label = Gtk.Label("HARDWARE -- This is a dialog to display additional information ")
        elif(text_type  == "load"):
            label = Gtk.Label("LOAD -- This is a dialog to display additional information ")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

def main():
    """ Main function """
    os.environ["ARCH"] = "x86_64"
    utility.match("x86_64")

if __name__ == "__main__":

    main()
    path = "/net/travail/jaupetit/linux-3.13.5/"

    # Version du noyau
    version = "3"
    patchlevel = "13"
    sublevel = "5"
    extraversion = ""

    os.environ["srctree"] = path

    os.environ["VERSION"] = version
    os.environ["PATCHLEVEL"] = patchlevel
    os.environ["SUBLEVEL"] = sublevel
    os.environ["EXTRAVERSION"] = extraversion

    os.environ["KERNELVERSION"] = version + "." + patchlevel + "." + sublevel

    c = kconfiglib.Config(filename=path+"Kconfig", base_dir=path, print_warnings=False)

    print "==== DEBUG ===="
    print ""
    print "Verification de l'architecture"
    print c.get_srcarch()
    print c.get_arch()

    print ""
    print "Vérification du chemin et de la version du noyau"
    print c.get_srctree()
    print os.environ.get("KERNELVERSION")
    print ""
    print "==== FIN DEBUG ===="
    print "==== Si utilisation dans un interpreteur (ipython par exemple) \
l'instance de la configuration kconfiglib est accessible dans \
la variable 'c' ===="

    ConfigurationInterface()
    Gtk.main()



# test
# c.load_config("../x86_64_defconfig")
# c.write_config(filename="TOTO")

"""
Faire une grosse classe MAIN qui ouvre les fenetres
Qui récupère les valeurs de retours de fenetre pour en ouvrir d'autres
Et cette classe stockera les informations nécessaire a l'application (options, option courante, ...)
"""
