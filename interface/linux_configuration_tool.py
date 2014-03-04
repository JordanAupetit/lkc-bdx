 #!/usr/bin/python

from gi.repository import Gtk

class KernelInterface():
	def __init__(self):
		self.interface = Gtk.Builder()
		self.interface.add_from_file('chooseKernel.glade')
		self.window = self.interface.get_object('mainWindow')
		self.toClose = True
		
		#self.btn_load = self.interface.get_object("btn_load")
		self.interface.connect_signals(self)

		print("Start")

	def on_mainWindow_destroy(self, widget):
		print("Window KernelInterface destroyed")
		if(self.toClose):
			Gtk.main_quit()
		else:
			self.toClose = True


	# On stop le chargement du Kernel
	def on_btn_stop_clicked(self, widget):
		print("Btn STOP clicked")

	# On load le kernel puis on passe a la fenetre suivante
	def on_btn_load_clicked(self, widget):
		# Load du Kernel <<<
		print("Kernel Loaded")
		ConfigurationInterface()

		self.toClose = False
		self.window.destroy()

		print("Window Switched")

	def on_btn_exit_clicked(self, widget):
		print("Btn EXIT clicked")
		self.window.destroy()



class ConfigurationInterface():
	def __init__(self):
		self.interface = Gtk.Builder()
		self.interface.add_from_file('chooseConfiguration.glade')
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

	# On retourne sur la fenetre du Load Kernel
	def on_btn_back_clicked(self, widget):
		KernelInterface()

		self.toClose = False
		self.window.destroy()

	def on_btn_next_clicked(self, widget):
		# Apply configuration <<<
		print("Configuration loaded")
		OptionsInterface()

		self.toClose = False
		self.window.destroy()

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


if __name__ == "__main__":
	KernelInterface()
	Gtk.main()