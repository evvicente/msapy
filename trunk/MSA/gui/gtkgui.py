#!/usr/bin/env python

import gtk
import sys

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()

        self.connect("destroy", gtk.main_quit)
        self.set_title("MSA")
        self.set_default_size(750,450)
        self.set_size_request(250, 200)
        self.set_position(gtk.WIN_POS_CENTER)

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        newtb = gtk.ToolButton(gtk.STOCK_NEW)
        opentb = gtk.ToolButton(gtk.STOCK_OPEN)
        savetb = gtk.ToolButton(gtk.STOCK_SAVE)
        sep = gtk.SeparatorToolItem()
        quittb = gtk.ToolButton(gtk.STOCK_QUIT)

        toolbar.insert(newtb, 0)
        toolbar.insert(opentb, 1)
        toolbar.insert(savetb, 2)
        toolbar.insert(sep, 3)
        toolbar.insert(quittb, 4)

        self.filename = ""
        self.textbox = gtk.TextView()
        
        self.textbox.set_wrap_mode(gtk.WRAP_WORD)
        self.textbox.set_editable(True)
        self.textbox.set_cursor_visible(True)        
        self.textbox.set_border_window_size(gtk.TEXT_WINDOW_LEFT,1)
        self.textbox.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,1)
        self.textbox.set_border_window_size(gtk.TEXT_WINDOW_TOP,1)
        self.textbox.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM,1)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledwindow.add(self.textbox)

        self.statusbar = gtk.Statusbar()
        
        newtb.connect("clicked", self.new_file)
        opentb.connect("clicked", self.open_file)
        savetb.connect("clicked", self.save_file)
        quittb.connect("clicked", gtk.main_quit)

        vbox = gtk.VBox(False, 2)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.pack_start(scrolledwindow, True, True, 0)
        vbox.pack_start(self.statusbar, False, False, 0)

        self.add(vbox)

        self.show_all()

    def new_file(self, user_param):
        self.set_title("Untitled - MSA")
        textbuffer = self.textbox.get_buffer()
        textbuffer.set_text("")
        self.statusbar.push(0, "New: Untitled")
        print "New: Untitled"
    
    def open_file(self, user_param):
        chooser = gtk.FileChooserDialog(title = "Open a file", 
                                        action = gtk.FILE_CHOOSER_ACTION_OPEN, 
                                        buttons = (gtk.STOCK_CANCEL, 
                                                   gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OPEN,
                                                   gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.filename = chooser.get_filename()
            textbuffer = self.textbox.get_buffer()
            index = self.filename.replace("\\","/").rfind("/") + 1
            self.set_title(self.filename[index:] + " - MSA")
            file = open(self.filename, "r")
            text = file.read()
            textbuffer.set_text(text)
            file.close()
            self.statusbar.push(0,"Opened File: " + self.filename)
            print "Opened File:", self.filename
        chooser.destroy()

    def save_file(self, user_param):
        
        textbuffer = self.textbox.get_buffer()
        index = self.filename.replace("\\","/").rfind("/") + 1
        text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
        self.set_title(self.filename[index:] + " - MSA")
        file = open(self.filename, "r+")
        file.write(text)
        file.close()
        self.statusbar.push(0, "Saved File: " + self.filename)
        print "Saved File:", self.filename

if __name__ == "__main__":
    PyApp()
    gtk.main()


"""             
def save_file_as(menuitem,user_param):
        chooser = gtk.FileChooserDialog(title="Save file",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
                chooser.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
                filter.set_name("Text Files")
                filter.add_mime_type("text/data")
                filter.add_pattern("*.txt")
                chooser.add_filter(filter)
        filter2 = gtk.FileFilter()
        filter2.set_name("All Files")
        filter2.add_pattern("*.*")
        chooser.add_filter(filter2)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
                global _File
                filename = chooser.get_filename()
                _File = filename
                textbuffer = TextBox.get_buffer()
                print "Saved File: " + filename
                        StatusBar.push(0,"Saved File: " + filename)
                index = filename.replace("\\","/").rfind("/") + 1
                text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
                window.set_title(filename[index:] + " - PyPad")
                file = open(filename, "w")
                file.write(text)
                file.close()
        elif response == gtk.RESPONSE_CANCEL:
                chooser.destroy()
                chooser.destroy()
"""