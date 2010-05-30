#!/usr/bin/env python

"""
class NotebookExample:

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.delete)
        window.set_border_width(10)

        table = gtk.Table(3,6,gtk.FALSE)
        window.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0,6,0,1)
        notebook.show()
        self.show_tabs = gtk.TRUE
        self.show_border = gtk.TRUE

        # Let's append a bunch of pages to the notebook
        for i in range(5):
            bufferf = "Append Frame %d" % (i+1)
            bufferl = "Page %d" % (i+1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            notebook.append_page(frame, label)
      
        # Now let's add a page to a specific spot
        checkbutton = gtk.CheckButton("Check me please!")
        checkbutton.set_size_request(100, 75)
        checkbutton.show ()

        label = gtk.Label("Add page")
        notebook.insert_page(checkbutton, label, 2)

        # Now finally let's prepend pages to the notebook
        for i in range(5):
            bufferf = "Prepend Frame %d" % (i+1)
            bufferl = "PPage %d" % (i+1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            notebook.prepend_page(frame, label)
    
        # Set what page to start at (page 4)
        notebook.set_current_page(3)

        # Create a bunch of buttons
        button = gtk.Button("close")
        button.connect("clicked", self.delete)
        table.attach(button, 0,1,1,2)
        button.show()

        button = gtk.Button("prev page")
        button.connect("clicked", lambda w: notebook.prev_page())
        table.attach(button, 2,3,1,2)
        button.show()

        button = gtk.Button("tab position")
        button.connect("clicked", self.rotate_book, notebook)
        table.attach(button, 3,4,1,2)
        button.show()

        button = gtk.Button("tabs/border on/off")
        button.connect("clicked", self.tabsborder_book, notebook)
        table.attach(button, 4,5,1,2)
        button.show()

        button = gtk.Button("remove page")
        button.connect("clicked", self.remove_book, notebook)
        table.attach(button, 5,6,1,2)
        button.show()

        table.show()
        window.show()
"""

import gtk

from pylab import *
from matplotlib.figure import Figure

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

import sys

class PyApp():
    def __init__(self):
        
        # Create toplevel window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("MSA")
        window.connect("destroy", gtk.main_quit)
        window.set_default_size(750,450)
        window.set_size_request(450, 400)
        window.set_border_width(2)
        window.set_position(gtk.WIN_POS_CENTER)

        # Create vbox widget for toplevel window
        vbox = gtk.VBox() #vbox = gtk.VBox(False, 2)               
        window.add(vbox)

        # Create toolbar
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        vbox.pack_start(toolbar, False, False, 0)
        
        # Create toolbuttons for toolbar
        newtb = gtk.ToolButton(gtk.STOCK_NEW)
        newtb.connect("clicked", self.new_file)
        opentb = gtk.ToolButton(gtk.STOCK_OPEN)
        opentb.connect("clicked", self.open_file)
        savetb = gtk.ToolButton(gtk.STOCK_SAVE)
        savetb.connect("clicked", self.save_file)
        runtb = gtk.ToolButton(gtk.STOCK_EXECUTE)
        helptb = gtk.ToolButton(gtk.STOCK_HELP)
        
        toolbar.insert(newtb, 0)
        toolbar.insert(opentb, 1)
        toolbar.insert(savetb, 2)
        toolbar.insert(gtk.SeparatorToolItem(), 3)
        toolbar.insert(runtb, 4)
        toolbar.insert(gtk.SeparatorToolItem(), 5)
        toolbar.insert(helptb, 6)
        
        # Create notebook and place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_RIGHT)
        vbox.pack_start(notebook)
        
        # Create toolbar
        toolbar = gtk.Toolbar()
        vbox.pack_start(toolbar, False, False)
        
        # Create previous tool button
        tbutton = gtk.ToolButton(gtk.STOCK_GO_BACK)
        tbutton.connect("clicked", lambda n:notebook.prev_page())
        toolbar.insert(tbutton, 0)
        # Create next tool button
        tbutton = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        tbutton.connect("clicked", lambda n:notebook.next_page())
        toolbar.insert(tbutton, 1)
        # Create separator
        toolbar.insert(gtk.SeparatorToolItem(), 2)
        # Create exit tool button
        tbutton = gtk.ToolButton(gtk.STOCK_QUIT)
        tbutton.connect("clicked", gtk.main_quit)
        toolbar.insert(tbutton, 3)
        
        # Create textbox and append as new notebook page
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
        #vbox.pack_start(scrolledwindow, True, True, 0)
        notebook.append_page(scrolledwindow, gtk.Label("editor"))
        
        """
        # Create a scrolled text area that displays a "message"
        view = gtk.TextView()
        buffer = view.get_buffer()
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(view)
        self.insert_text(buffer)
        scrolled_window.show_all()
        return scrolled_window
        """
        
        # Create matplotlib FigureCanvasGTK widget to gtk notebook page
        vbox = gtk.VBox()
        notebook.append_page(vbox, gtk.Label("Plot"))
        
        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        ax.plot(t,s, label="seno")
        legend()
        ax.grid(True)
        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        #vbox.pack_start(canvas, True, True, 0)
        vbox.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, window)
        vbox.pack_start(toolbar, False, False)
        
        # Create and append notebook page
        frame = gtk.Frame()
        frame.set_border_width(10)
        frame.set_size_request(100, 75)
        
        notebook.append_page(frame, gtk.Label("log"))
        
        # Show all
        window.show_all()

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
            #self.set_title(self.filename[index:] + " - MSA")
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