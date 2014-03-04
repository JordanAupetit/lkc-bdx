 #!/usr/bin/python

from gi.repository import Gtk

class LinuxConfigurationTool:
	def __init__(self):
		self.interface = Gtk.Builder()
		self.interface.add_from_file('chooseKernel.glade')
		#self.interface.add_from_file('chooseConfiguration.glade')
		#self.interface.add_from_file('chooseOptions.glade')
		
		self.btn_load = self.interface.get_object("btn_load")
		self.interface.connect_signals(self)

		print("Start")

	def on_mainWindow_destroy(self, widget):
		Gtk.main_quit()
		print("Window destroyed")

	def on_btn_stop_clicked(self, widget):
		print("Btn STOP clicked")

	def on_btn_load_clicked(self, widget):
		print("Btn LOAD clicked")
		#self.interface.add_from_file('chooseConfiguration.glade')

	def on_btn_exit_clicked(self, widget):
		print("Btn EXIT clicked")
		Gtk.main_quit()

if __name__ == "__main__":
	LinuxConfigurationTool()
	Gtk.main()