#!/usr/bin/env python2
 # -*- coding: utf-8 -*-

#(’°O°)’

from gi.repository import Gtk

import os
import sys
import re

sys.path.append("modules/")
import utility
import search
sys.path.append("parser/")
import kconfiglib


#   ==========================
#   ==== TODO 
#   ==========================
#
#   - Voir si on peut améliorer le chargement du kconfig avec un Thread
#
#   - On ne traite ici QUE l'affichage des symboles 
#   (et des symboles dans les menus) et pas des menus, choice or comment
#
#   - Mettre des bornes pour le Back et Next pour le déplacements dans les 
#   options                                                ===> OK (A revoir) <===

#   - Virer les commentaires inutiles
#
#   - ATTENTION, dans certaines Arch, comme frc et alpha, le dossier configs
#   n'existe pas, il y a un fichier defconfig a la racine de l'archi
#
#   - Envisager d'enlever du code non lié a GTK pour le mettre dans des modules
#
#   - Modifier la taille des blocs dans la fenetres pour une meilleur
#   visibilité
#
#   - Filtrer l'affichage dans recherche pour ne pas afficher les options
#   non modifiable
#
#   - Lorsque l'on est sur un Menu dans la Recherche, utiliser un bouton
#   pour développer le Menu (ie ENTER)
#
#   - Pour la partie section, regrouper les options par Menu et afficher
#   les menus
#
#   - Rajouter deux boutons pour EXPAND et UNEXPAND la liste des options
#
#   - Quand on ferme la fenetre où que l'on fait Finish, demander a 
#   l'utilisateur de confirmer (petit pop-up)
#
#   - Faire des TESTS avec différents Kernel 2.* et 3.* pour tester que l'on
#   récupère toujours les Architecture et les fichiers configs
#
#   - Interessant de déplacer le curseur de la recherche quand on appuie sur
#   next, également valable pour le menu de SECTION
#   
#
#   =============================================================
#   =======================> PRIORITAIRE <=======================
#
#   - Lors d'un Conflit, mettre en évidence l'onglet conflit (couleur rouge ?)
#
#   - Ajouter des TESTS sur les fichiers mis dans l'input config (et les autres)
#
#   - Lors du Defconfig lever une erreur en cas où le chemin vers le fichier 
#   ne soit pas le bon
#
#   - Envisager d'afficher le menu dans lequel se trouve l'option
#
#   - Probleme modification valeur CHOICE "Compile the kernel with frame" =>
#   HEXAGON_COMET
#
#   - Afficher l'architecture courante
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

        self.input_choose_kernel.set_text(self.app_memory["path"])

        path = self.input_choose_kernel.get_text()
        if os.path.exists(path):
            list_arch = os.listdir(path + "/arch")
            self.combo_text_archi_folder.set_sensitive(True)
            self.combo_text_archi_folder.remove_all()
            self.combo_text_archi_defconfig.set_sensitive(False)
            self.combo_text_archi_defconfig.remove_all()

            i = 0
            arch_i = 0
            for arch in list_arch:
                if arch == app_memory["archi_folder"]:
                    arch_i = i
                if(os.path.isdir(path + "/arch/" + arch)):
                    self.combo_text_archi_folder.append_text(arch)
                    i = i + 1

            self.combo_text_archi_folder.set_active(arch_i)

            path = app_memory["path"] + "arch/" + app_memory["archi_folder"]
            if os.path.exists(path + "/configs"):
                path += "/configs"

            if os.path.exists(path):
                list_arch = os.listdir(path)
                self.combo_text_archi_defconfig.set_sensitive(True)
                self.combo_text_archi_defconfig.remove_all()
                
                i = 0
                arch_i = 0
                for arch in list_arch:
                    if arch == app_memory["archi_defconfig"]:
                        arch_i = i
                    if not (os.path.isdir(path + "/" + arch)):
                        self.combo_text_archi_defconfig.append_text(arch)
                        i = i + 1
            
                self.combo_text_archi_defconfig.set_active(arch_i)


    def on_mainWindow_destroy(self, widget):
        if (self.toClose):
            app_memory["open"] = False

        Gtk.main_quit()


    def on_btn_choose_kernel_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.input_choose_kernel.set_text(dialog.get_filename())

        dialog.destroy()


    def on_input_choose_kernel_changed(self, widget):
        path = self.input_choose_kernel.get_text()
        if os.path.exists(path):
            list_arch = os.listdir(path + "/arch")
            self.combo_text_archi_folder.set_sensitive(True)
            self.combo_text_archi_folder.remove_all()
            self.combo_text_archi_defconfig.set_sensitive(False)
            self.combo_text_archi_defconfig.remove_all()

            for arch in list_arch:
                if(os.path.isdir(path + "/arch/" + arch)):
                    self.combo_text_archi_folder.append_text(arch)

        else:
            self.combo_text_archi_folder.set_sensitive(False)


    def on_combo_text_archi_folder_changed(self, widget):
        path = self.input_choose_kernel.get_text()
        arch_active = self.combo_text_archi_folder.get_active_text()

        if(path[len(path) - 1] != "/"):
            path += "/"

        if arch_active != None :
            path_list_arch_defconfig = path + "arch/" + arch_active

            if os.path.exists(path_list_arch_defconfig + "/configs/"):
                list_arch_defconfig = os.listdir(path_list_arch_defconfig + \
                    "/configs/")
                self.srcdefconfig = path_list_arch_defconfig + "/configs/"
                self.combo_text_archi_defconfig.set_sensitive(True)
                self.combo_text_archi_defconfig.remove_all()

                for arch in list_arch_defconfig:
                    self.combo_text_archi_defconfig.append_text(arch)

            elif os.path.isfile(path_list_arch_defconfig + "/defconfig"):
                self.srcdefconfig = path_list_arch_defconfig + "/"
                self.combo_text_archi_defconfig.set_sensitive(True)
                self.combo_text_archi_defconfig.remove_all()
                self.combo_text_archi_defconfig.append_text("defconfig")

            else:
                self.srcdefconfig = ""
                self.combo_text_archi_defconfig.set_sensitive(False)


    def on_btn_choose_config_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.input_choose_config.set_text(dialog.get_filename())
        #elif response == Gtk.ResponseType.CANCEL:
            #print("Cancel clicked")

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
        print("Nothing")


    #error
    def on_btn_next_clicked(self, widget):

        if (self.input_choose_kernel.get_text() == "" or
            self.combo_text_archi_folder.get_active_text() == None or
            self.combo_text_archi_defconfig.get_active_text() == None):
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
        #path = "/net/travail/jaupetit/linux-3.13.5/"

        if(path[len(path) - 1] != "/"):
            path += "/"

        # initialisation de l'environement
        arch = self.combo_text_archi_defconfig.get_active_text()
        srcarch = self.combo_text_archi_folder.get_active_text()
        self.srcdefconfig += self.combo_text_archi_defconfig.get_active_text()
        utility.init_environ(path, arch, srcarch, self.srcdefconfig)

        kconfig_infos = kconfiglib.Config(filename=path+"Kconfig",
            base_dir=path, print_warnings=False)

        print "Verification de l'architecture"
        print kconfig_infos.get_srcarch()
        print kconfig_infos.get_arch() + "\n"

        print "Vérification du chemin et de la version du noyau"
        print kconfig_infos.get_srctree()
        print os.environ.get("KERNELVERSION") + "\n"

        if (self.radio_state == "default"):
            print("Configuration by default")
            kconfig_infos.load_config(self.srcdefconfig)
        elif (self.radio_state == "load"):
            print("Configuration by load")
            kconfig_infos.load_config(self.input_choose_config.get_text())

        app_memory["kconfig_infos"] = kconfig_infos

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


class OptionsInterface():
    def __init__(self, app_memory):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('interface/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory
        self.current_option_index = -1
        self.previous_options = []

        # For tree displaying
        self.treestore_search = Gtk.TreeStore(str)
        self.treeview_search = Gtk.TreeView(model=self.treestore_search)

        self.treestore_section = Gtk.TreeStore(str)
        self.treeview_section = Gtk.TreeView(model=self.treestore_section)

        self.move_cursor_allowed = True # Cursor list options

        self.top_level_items = \
            app_memory["kconfig_infos"].get_top_level_items()
        self.items = []
        utility.get_all_items(self.top_level_items, self.items)

        # # ===========
        # # == DEBUG ==
        #
        print len(self.items)
        #
        # for i in self.items:
        #     self.current_option_index += 1
        #     current_item = self.items[self.current_option_index]

        #     print "Option ", self.current_option_index, " | ", \
        #         "Name => ", current_item.get_name(), " | ", \
        #         "Value => ", current_item.get_value(), " | ", \
        #         current_item.get_assignable_values(), " | ", \
        #         current_item.get_type()

        # ============================

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

        self.btn_back.set_sensitive(False)

        self.add_tree_view()
        # Initialisation de l'arbre des options
        self.get_tree_option(self.top_level_items)
        self.add_section_tree()

        self.interface.connect_signals(self)


    def on_mainWindow_destroy(self, widget):
        print("Window ConfigurationInterface destroyed")
        if (self.toClose):
            app_memory["open"] = False

        Gtk.main_quit()


    def on_btn_back_clicked(self, widget):
        if len(self.previous_options) > 0:
            self.current_option_index = \
                self.previous_options[len(self.previous_options) - 1]

            self.previous_options.pop()

            self.change_option()

        if len(self.previous_options) <= 0:
            self.btn_back.set_sensitive(False)


    def on_btn_next_clicked(self, widget):
        self.set_value_option()
        old_position = self.current_option_index
        if self.current_option_index >= 0:
            self.previous_options.append(self.current_option_index)

        self.current_option_index += 1
        show = False

        self.show_interface_option()

        while(show == False):
            if(self.current_option_index > (len(self.items) - 1)):
                self.current_option_index = old_position
                self.btn_next.set_sensitive(False)

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

        if self.items[self.current_option_index].get_value() != radio_type and \
            self.items[self.current_option_index].is_modifiable() == False:
            self.btn_next.set_sensitive(False)


    def on_combo_choice_changed(self, widget):
        self.btn_next.set_sensitive(True)
        current_item = self.items[self.current_option_index]
        active_text = self.combo_choice.get_active_text()
        selection = current_item.get_selection()

        if current_item.get_visibility() == "n":
            if selection == None:
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
        self.move_cursor_allowed = False
        self.treestore_search.clear()
        self.move_cursor_allowed = True

        for current_name, current_item in r:
            if current_item.is_choice() or current_item.is_symbol():
                description = current_item.get_prompts()
                
                option = "<" + current_name + ">"
                if description:
                    option = description[0] + " :: " + option
                self.treestore_search.append(None, [option])
                i += 1

        self.change_title_column_treeview \
            (str(i) + " results for \"" + pattern + "\"", 0)
        #print "résultat : " + str(i) + " option(s) trouvées"


    def get_tree_option(self, items, parent=None):
        self.move_cursor_allowed = False
        self.treestore_search.clear()
        self.move_cursor_allowed = True

        self.change_title_column_treeview \
            ("Complete list of options (" + str(len(self.items)) + ")", 0)
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
                    self.treestore_search.append(parent, [str(item.get_prompts()[0])])
                    # choice = self.treestore_search.append(parent, [str(item.get_prompts()[0])])
                    # self.get_tree_options_rec(item.get_items(), choice)
            
            #elif item.is_comment():
            #    print "FIXME -- Comment in tree"
            # /net/travail/jaupetit/linux-3.13.5/

            # FIXME il y a des Comments a traiter


    def on_btn_finish_clicked(self, widget):
        app_memory["kconfig_infos"].write_config(".config")
        self.window.destroy()


    def change_option(self):
        current_item = self.items[self.current_option_index]

        help_text = current_item.get_help()

        if (help_text != None):
            self.label_description_option.set_text(help_text)
        else:
            self.label_description_option.set_text("No help available.")

        if current_item.is_symbol():
            self.label_title_option \
                .set_text("[Option n°" + str(self.current_option_index) + \
                    "] Do you want " + current_item.get_name() + \
                    " option enabled ?")

            # ===============
            # == DEBUG ======

            assignable_values = current_item.get_assignable_values()

            print "Option ", self.current_option_index, " | ", \
                    "Name => ", current_item.get_name(), " | ", \
                    current_item.is_modifiable(), " | ", \
                    current_item.get_visibility(), " | ", \
                    "Value => ", current_item.get_value(), " | ", \
                    current_item.get_assignable_values(), " | ", \
                    current_item.get_type()

            print "Description ", current_item.get_prompts()

            id_type = current_item.get_type()
            item_type = ""
                    
            if id_type == kconfiglib.BOOL:
                item_type = "BOOL"
            elif id_type == kconfiglib.TRISTATE:
                item_type = "TRISTATE"
            elif id_type == kconfiglib.STRING:
                item_type = "STRING"
            elif id_type == kconfiglib.HEX:
                item_type = "HEX"
            elif id_type == kconfiglib.INT:
                item_type = "INT"                                  

            print "Type : " + item_type
            # ===============

            value = current_item.get_value()

            if (value == "y"):
                self.radio_yes.set_active(True)
            if (value == "m"):
                self.radio_module.set_active(True)
            if (value == "n"):
                self.radio_no.set_active(True)

            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)
            self.combo_choice.set_visible(False)


            # Enabling few radio button
            if (current_item.get_type() == kconfiglib.BOOL):
                self.radio_yes.set_visible(True)
                self.radio_no.set_visible(True)
            elif (current_item.get_type() == kconfiglib.TRISTATE):
                self.radio_yes.set_visible(True)
                self.radio_module.set_visible(True)
                self.radio_no.set_visible(True)

        elif current_item.is_choice():

            if len(current_item.get_prompts()) > 0:
                self.label_title_option \
                    .set_text("[Option n°" + str(self.current_option_index) + \
                        "] Do you want to change the selected \
option of this choice ? \n" + current_item.get_prompts()[0])
            else:
                self.label_title_option \
                .set_text("[Option n°" + str(self.current_option_index) + \
                    "] Do you want to change the selected option of this choice ?")

            # ===============
            # == DEBUG ======

            print "Option ", self.current_option_index, " | Choice <<=="
            print "Visibility choice => " + current_item.get_visibility()

            # ===============

            # Disabling each radio button
            self.radio_yes.set_visible(False)
            self.radio_module.set_visible(False)
            self.radio_no.set_visible(False)

            self.combo_choice.set_visible(True)

            self.combo_choice.remove_all()

            self.combo_choice.append_text("No choice are selected")
            self.combo_choice.set_active(0)

            index = 1
            for item in current_item.get_symbols():
                self.combo_choice.append_text(item.get_name())
                if item.get_value() == "y":
                    self.combo_choice.set_active(index)
                index += 1


    def change_title_column_treeview(self, title, id_column):
        column = self.treeview_search.get_column(id_column)
        column.set_title(title)


    def add_tree_view(self, title="List of options"):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(title, renderer_text, text=0)
        self.treeview_search.append_column(column_text)
        self.treeview_search.set_enable_search(False)
        self.treeview_search.connect("cursor-changed", self.on_cursor_treeview_search_changed)

        scrolledwindow_search = self.interface.get_object("scrolledwindow_search")
        scrolledwindow_search.add(self.treeview_search)
        scrolledwindow_search.show_all()

    def add_section_tree(self):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Sections", renderer_text, text=0)
        self.treeview_section.append_column(column_text)
        self.treeview_section.set_enable_search(False)
        self.treeview_section.connect("cursor-changed", self.on_cursor_treeview_section_changed)

        scrolledwindow_search = self.interface.get_object("scrolledwindow_section")
        scrolledwindow_search.add(self.treeview_section)
        scrolledwindow_search.show_all()


    def on_cursor_treeview_search_changed(self, widget):
        if self.move_cursor_allowed:
            current_column = 0 # Only one column
            (treestore, indice) = widget.get_selection().get_selected()

            if indice != None:
                option_description = treestore[indice][current_column]

                result = re.search('<(.*)>' , option_description)
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
                    else: # Choice
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
                    self.change_option()

    def on_cursor_treeview_section_changed(self, widget):
        print ""


class DialogHelp(Gtk.Dialog):
    def __init__(self, parent, text_type):
        Gtk.Dialog.__init__(self, "Information", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Erreur")

        if (text_type  == "default"):
            label = Gtk.Label("DEFAULT -- This is a dialog to \
display additional information ")
        elif (text_type  == "load"):
            label = Gtk.Label("LOAD -- This is a dialog to \
display additional information ")
        elif (text_type  == "error_load_kernel"):
            label = Gtk.Label("Error -- You haven't completed the Linux \
Kernel field \n and/or the Architecture field.")
        elif (text_type  == "error_load_config"):
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
    app_memory["path"] = ""
    app_memory["archi_folder"] = ""
    app_memory["archi_defconfig"] = ""
    
    if len(sys.argv) >= 2:
        if os.path.exists(sys.argv[1]):
            path = sys.argv[1]
            if path[len(path)-1] != "/":
                path += "/"
            app_memory["path"] = path
            
        if len(sys.argv) >= 3:
            path = app_memory["path"] + "arch/" + sys.argv[2] + "/"
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
