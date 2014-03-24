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
#   Change current page notebook       ===> OK <===
#
#   - Ajouter des TESTS sur les fichiers mis dans l'input config (et les autres)
#
#   - Lors du Defconfig lever une erreur en cas où le chemin vers le fichier 
#   ne soit pas le bon
#
#   - Envisager d'afficher le menu dans lequel se trouve l'option
#                                      ===> OK <===
#
#   - Probleme modification valeur CHOICE "Compile the kernel with frame" 
#   HEXAGON_COMET    ===> OK <===
#
#   - Afficher l'architecture courante ===> OK <===
#
#   - Verifier que les Menus ne sont pas des Bool pour les activer desactiver
#   (Normalement PAS de problèmes)
#
#

# =============================================================================

#						T E S T S    U N I T A I R E S

# =============================================================================


# Vérification du fonctionnement de la liste de dépendance pour une option
# ------------------------------------------------------------------------

# Attendu : Pas de crash de l'application

def tu_test01(optInter, radio_type):

    for i in range(1600):
        if not isinstance(optInter.items[optInter.current_option_index],\
        kconfiglib.Choice): # en attendant qu'on regle le pb avec les choix
            optInter.change_interface_conflit("?")
            optInter.on_btn_next_clicked(radio_type)

# Vérification de la validité de la liste de dépendance lorsqu'elle est vide
#---------------------------------------------------------------------------

# Attendu : Aucun résultat, on est pas censé avoir des conflits
# 		    alors que la liste des conditions est vide

# info : linux_configuration_tool.py | grep dep vide | wc
# -----> Donne le nombre d'erreur


def tu_test02(optInter, radio_type):

    for i in range(1600):
        if not isinstance(optInter.items[optInter.current_option_index],\
        kconfiglib.Choice): # en attendant qu'on regle le pb avec les choix

            local_opt_name =  optInter.items[optInter.current_option_index].get_name()
            cur_opt = utility.SymbolAdvance(optInter.app_memory["kconfig_infos"]\
                                            .get_symbol(local_opt_name))
        
            list_conflicts = cur_opt.cat_symbols_list()

            if list_conflicts == [] and \
            optInter.items[optInter.current_option_index].get_visibility() == "n":
                print "TU_TEST02a : <",local_opt_name,"> : ERROR : dep vide et conflit"

            optInter.change_interface_conflit("?")
            optInter.on_btn_next_clicked(radio_type)
                

#  
#---------------------------------------------------------------------------

# Attendu : 
        
#def tu_test03(optInter, radio_type):


#
#---------------------------------------------------------------------------
        
#def tu_test04(optInter, radio_type):
            

#     
# =============================================================================


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

        self.input_choose_kernel.set_text(self.app_memory["kernel_path"])

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

            path = app_memory["kernel_path"] + "arch/" + app_memory["archi_folder"]
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
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.input_choose_kernel.set_text(dialog.get_filename())

        dialog.destroy()


    def on_input_choose_kernel_changed(self, widget):
        path = self.input_choose_kernel.get_text()

        self.combo_text_archi_folder.remove_all()
        self.combo_text_archi_defconfig.remove_all()
        self.combo_text_archi_defconfig.set_sensitive(False)

        if os.path.exists(path):
            list_arch = os.listdir(path + "/arch")
            self.combo_text_archi_folder.set_sensitive(True)

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
        print "Nothing"


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


class OptionsInterface(Gtk.Window):
    def __init__(self, app_memory):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('interface/chooseOptions.glade')
        self.window = self.interface.get_object('mainWindow')
        self.toClose = True
        self.app_memory = app_memory
        self.current_option_index = -1
        self.previous_options = []

        self.window.set_title("Linux Kernel Configuration - Architecture : " + \
                              app_memory["kconfig_infos"].get_srcarch())

        # For tree displaying
        self.treestore_search = Gtk.TreeStore(str)
        self.treeview_search = Gtk.TreeView(model=self.treestore_search)

        self.treestore_section = Gtk.TreeStore(str)
        self.treeview_section = Gtk.TreeView(model=self.treestore_section)

        self.treestore_conflicts = Gtk.TreeStore(str)
        self.treeview_conflicts = Gtk.TreeView(model=self.treestore_conflicts)

        self.move_cursor_search_allowed = True # Cursor list options
        self.move_cursor_section_allowed = True 
        self.move_cursor_conflicts_allowed = True 

        self.top_level_items = \
            app_memory["kconfig_infos"].get_top_level_items()
        self.menus = app_memory["kconfig_infos"].get_menus()
        self.top_menus = utility.get_top_menus(self.menus)
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
        self.label_current_menu = self.interface.get_object("label_current_menu")
        self.notebook = self.interface.get_object("notebook2")

        self.btn_back.set_sensitive(False)

        self.add_tree_view()
        # Initialisation de l'arbre des options
        self.get_tree_option(self.top_level_items)
        self.add_section_tree()
        self.add_conflicts_tree()

        self.interface.connect_signals(self)
        
    def on_mainWindow_delete_event(self, widget, data):
        self.on_menu1_quit_activate(widget)
        return True
    
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

            self.btn_next.set_sensitive(True)
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


    def on_radio_yes_clicked(self, widget):
        self.change_interface_conflit("y")


    def on_radio_module_clicked(self, widget):
        self.change_interface_conflit("m")


    def on_radio_no_clicked(self, widget):
        self.change_interface_conflit("n")



    def change_interface_conflit(self, radio_type):

        # print "----------------------------"
        # print self.items[self.current_option_index].prompts
        # print "++++++++++++++++++++++++++++"

        # --- condition utile pour test unitaire ---

        self.btn_next.set_sensitive(True)
        self.move_cursor_conflicts_allowed = False
        self.treestore_conflicts.clear()
        self.move_cursor_conflicts_allowed = True

        if self.items[self.current_option_index].get_value() != radio_type and \
            self.items[self.current_option_index].is_modifiable() == False:
            self.btn_next.set_sensitive(False)

            local_opt_name =  self.items[self.current_option_index].get_name()
            cur_opt = utility.SymbolAdvance(\
                                        self.app_memory["kconfig_infos"]\
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
                if (find and
                    (self.items[cpt].get_type() == kconfiglib.BOOL or
                    self.items[cpt].get_type() == kconfiglib.TRISTATE)):

                    self.treestore_conflicts.append(None, ["<" + conflit + "> -- Value(" + str(self.items[cpt].get_value()) + ")"])
                else:
                    print "CONFLICT not bool or tristate"

            if list_conflicts != []:
                self.notebook.set_current_page(2) # 2 => Conflicts page

        

        if radio_type == "?":
            self.btn_next.set_sensitive(True)

        #print "======== > > ==== ", local_opt_name

                                        
        #                                ARCH_SPARSEMEM_ENABLE

        #string_symbol_list = str(utility.cat_symbols_list(cur_opt))

        #print cur_opt.cat_symbols_list()
        

        #label_conflicts.set_text(string_symbol_list)



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
        #print "résultat : " + str(i) + " option(s) trouvées"


    def get_tree_option(self, items, parent=None):
        self.move_cursor_search_allowed = False
        self.treestore_search.clear()
        self.move_cursor_search_allowed = True

        self.change_title_column_treeview \
            ("Complete list of options : " + str(len(self.items)), 0)
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
                    self.treestore_search.append(\
                        parent, [str(item.get_prompts()[0])])
                    # choice = self.treestore_search.append(\
                    #    parent, [str(item.get_prompts()[0])])
                    # self.get_tree_options_rec(item.get_items(), choice)
            
            #elif item.is_comment():
            #    print "FIXME -- Comment in tree"
            # /net/travail/jaupetit/linux-3.13.5/

            # FIXME il y a des Comments a traiter


    def on_btn_finish_clicked(self, widget):
        self.on_menu1_quit_activate(widget)


    def change_option(self):
        current_item = self.items[self.current_option_index]

        help_text = current_item.get_help()

        self.move_cursor_conflicts_allowed = False
        self.treestore_conflicts.clear()
        self.move_cursor_conflicts_allowed = True

        if (help_text != None):
            self.label_description_option.set_text(help_text)
        else:
            self.label_description_option.set_text("No help available.")

        self.move_cursor_section_allowed = False
        index_menu_option = utility.get_index_menu_option(\
            self.current_option_index, self.items, self.top_menus)
        self.treeview_section.set_cursor(index_menu_option)
        self.move_cursor_section_allowed = True

        self.label_current_menu.set_visible(True)
        if current_item.get_parent() == None:
            self.label_current_menu.set_text("Current menu : General options")
        else:   
            self.label_current_menu.set_text("Current menu : " + \
                current_item.get_parent().get_title())


        if current_item.is_symbol():
            text = "[Option n°" + str(self.current_option_index) + "] "
            text += "Do you want " + current_item.get_name() + \
                " option enabled ?"
            self.label_title_option.set_text(text)

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
                text = "[Option n°" + str(self.current_option_index) + "] "
                text += "Do you want to change the selected option of this choice ? \n"
                text += current_item.get_prompts()[0]
                self.label_title_option.set_text(text)
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

        scrolledwindow_section = self.interface.get_object("scrolledwindow_section")
        scrolledwindow_section.add(self.treeview_section)

        self.treestore_section.append(None, ["General options (options without menu)"])

        for m in self.top_menus:
            self.treestore_section.append(None, [m.get_title()])

        scrolledwindow_section.show_all()


    def add_conflicts_tree(self):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Conflicts", renderer_text, text=0)
        self.treeview_conflicts.append_column(column_text)
        self.treeview_conflicts.set_enable_search(False)
        self.treeview_conflicts.connect("cursor-changed", self.on_cursor_treeview_conflicts_changed)

        scrolledwindow_conflicts = self.interface.get_object("scrolledwindow_conflicts")
        scrolledwindow_conflicts.add(self.treeview_conflicts)

        scrolledwindow_conflicts.show_all()


    def on_cursor_treeview_search_changed(self, widget):
        if self.move_cursor_search_allowed:
            current_column = 0 # Only one column
            
            if not widget.get_selection():
                return

            (treestore, index) = widget.get_selection().get_selected()

            if index != None:
                option_description = treestore[index][current_column]

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
                    self.btn_next.set_sensitive(True)
                    self.change_option()


    def on_cursor_treeview_section_changed(self, widget):
        if self.move_cursor_section_allowed:
            if not widget.get_selection():
                    return

            current_column = 0 # Only one column
            (treestore, index) = widget.get_selection().get_selected()

            if index != None:
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
            current_column = 0 # Only one column
            
            if not widget.get_selection():
                return

            (treestore, index) = widget.get_selection().get_selected()

            if index != None:
                option_description = treestore[index][current_column]

                result = re.search('<(.*)>' , option_description)
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

            if app_memory["modified"] == True:
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

            if app_memory["modified"] == True:
                app_memory["modified"] = False
        
        save_as_dialog.destroy()
        
    def on_menu1_quit_activate(self, widget):
        if app_memory["modified"]:
            save_btn = "Save"
            label = Gtk.Label("Do you want to save the modifications of the " + \
                              "kernel configuration file" + \
                              " «" + app_memory["config_name"] + "» " + \
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

        # va faire tes tests ailleurs, péon
        #tu_test01(self, widget)
        #tu_test02(self, widget)
        # C'est toi le péon, tu codes comme un tequel nain, go skill shop !
    

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







