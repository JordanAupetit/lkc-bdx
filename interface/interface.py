 #!/usr/bin/python

from gi.repository import Gtk

class HelloWorld:
	def __init__(self):
		interface = Gtk.Builder()
		#interface.add_from_file('chooseKernel.glade')
		#interface.add_from_file('chooseConfiguration.glade')
		interface.add_from_file('chooseOptions.glade')
		
	# 	self.myLabel = interface.get_object("label1")
	# 	interface.connect_signals(self)

	# def on_mainWindow_destroy(self, widget):
	# 	Gtk.main_quit()

	# def on_button_clicked(self, widget):
	# 	self.myLabel.set_text("World!")
	# 	print("\"Click me\" button was clicked")

if __name__ == "__main__":
	HelloWorld()
	Gtk.main()