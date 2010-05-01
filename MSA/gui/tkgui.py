#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import webbrowser
import re # Expresiones regulares

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Tkinter as tk
import tkFileDialog

import msa

ICONSDIR = os.path.join(os.path.dirname(__file__), 'icons')
HELPDIR = os.path.join(os.path.dirname(__file__), '..', 'msa', 'help')
HELPFILE = os.path.join(HELPDIR, 'index.html')
DATADIR = os.path.join(os.path.dirname(__file__), '..', 'msa', 'data', 'examples')
XLSTEMPLATEFILE = os.path.join(DATADIR, 'input.xls')

class Gui():
    def __init__(self, window):
        self.window = window
        self.joints = []
        self.members = []
        self.filename = os.path.join(DATADIR, "input.csv")
        # Menu
        menu_frame = tk.Frame(window)
        menu_frame.grid(row=0, column=0,
                        sticky=tk.W+tk.E+tk.N+tk.S, padx=3, pady=2)
        # Open file
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'open.gif'))
        button = tk.Button(menu_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=self.open_file)
        button.image = img
        button.pack(side='left')
        # Save file
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'save.gif'))
        button = tk.Button(menu_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=self.save_file)
        button.image = img
        button.pack(side='left', padx=5)
        # Help
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'help.gif'))
        button = tk.Button(menu_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=lambda:webbrowser.open(HELPFILE))
        button.image = img
        button.pack(side='right')
        # Template
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'excel.gif'))
        button = tk.Button(menu_frame, image=img, text="        ",
                           compound='center', relief=tk.GROOVE,
                           command=lambda:os.system(XLSTEMPLATEFILE))
        button.image = img
        button.pack(side='right', padx=10)
        # PLot
        self.plot_frame = tk.Frame(window)
        self.plot_frame.grid(row=1, column=0)
        self.fig = matplotlib.pyplot.figure(1, figsize=(8.14, 4.73))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill='both', expand='yes')
        # Text
        self.text_frame = tk.Frame(window)
        self.text_frame.grid(row=1, column=0)
        scrollbar = tk.Scrollbar(self.text_frame)
        self.text = tk.Text(self.text_frame,
                            fg='darkorange', bg='#FAFAFA', font="Courier 10")
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill=tk.Y)
        self.text.pack(fill='both', expand='yes')
        # Tools
        tools_frame = tk.Frame(window)
        tools_frame.grid(row=2, column=0, sticky=tk.W, padx=3, pady=4)
        # Show editor
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'editor.gif'))
        self.button_editor = tk.Button(tools_frame, image=img, text=" ",
                                       compound='center', bg='gray',
                                       relief=tk.GROOVE,
                                       command=self.show_editor)
        self.button_editor.image = img
        self.button_editor.grid(row=0, column=0)
        # Show schematic
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'schematic.gif'))
        self.button_schematic = tk.Button(tools_frame, image=img, text=" ",
                                          compound='center', bg='gray',
                                          relief=tk.GROOVE,
                                          command=self.show_schematic)
        self.button_schematic.image = img
        self.button_schematic.grid(row=0, column=0)
        # Search
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'exec.gif'))
        button = tk.Button(tools_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=self.exec_msa)
        button.image = img
        button.grid(row=0, column=1, padx=5)
        # Solver
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'solve.gif'))
        button = tk.Button(tools_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=self.solve_msa)
        button.image = img
        button.grid(row=0, column=2, padx=5, ipadx=2, ipady=2)
        # Exit
        img = tk.PhotoImage(file=os.path.join(ICONSDIR, 'exit.gif'))
        button = tk.Button(tools_frame, image=img, text=" ",
                           compound='center', bg='gray', relief=tk.GROOVE,
                           command=lambda:self.window.quit())
        button.image = img
        button.grid(row=0, column=3, padx=20, ipadx=4, ipady=2)
        # Open default file
        self.open_file(name=self.filename)
    
    def open_file(self, name=""):
        """Abre un archivo"""
        try:
            msa.ui.info(">> Leyendo datos de definicion de la estructura... ")
            if not name:
                file = tkFileDialog.askopenfile(mode='r')
            else:
                file = open(name, "r")
            content = file.read()
            self.text.delete(tk.CURRENT, tk.END)
            self.text.insert(tk.CURRENT, content)
            self.filename = file.name
            self.window.title("MSA - " + self.filename)
            (self.joints,
             self.members,
             self.sections) = msa.load_data(self.filename)
            msa.ui.info(">> El archivo se ha cargado con exito ")
        except:
            msa.ui.error(">> No se ha podido abrir el archivo ")
    
    def save_file(self, name=""):
        """Guarda un archivo"""
        msa.ui.info(">> Guardando datos de definicion de la estructura... ")
        try:
            if not name:
                file = tkFileDialog.asksaveasfile(mode='w',
                                                  defaultextension=".csv")
            else:
                file = open(name, "w")
            contents = str(self.text.get(0.0, tk.END)).strip('\n')
            file.write(contents)
            file.close()
            self.filename = file.name
            msa.ui.info(">> El archivo se ha guardado con exito")
        except:
            msa.ui.error(">> No se ha podido guardar el archivo")
            
    def save_and_reload_if_changed(self):
        if self.text.edit_modified():
            msa.ui.info(">> Guardando datos modificados... ")
            self.save_file(self.filename)
            self.text.delete('1.0', tk.END)
            content = open(self.filename, 'r').read()           
            self.text.insert(tk.CURRENT, content)
            msa.ui.info(">> Recargando datos... ")
            (self.joints,
             self.members,
             self.sections) = msa.load_data(self.filename)
            msa.ui.info(">> El archivo se ha cargado con exito ")

    def show_editor(self):
        """Muestra el editor de texto"""
        self.plot_frame.lower()
        self.button_editor.lower()
        self.text_frame.lift()
        self.button_schematic.lift()

    def show_schematic(self):
        """Guarda los datos y muestra el esquema estructural"""
        self.text_frame.lower()
        self.button_schematic.lower()
        self.plot_frame.lift()
        self.button_editor.lift()
        self.fig.clear()
        msa.mpldraw.show_schematic(self.joints, self.members)
        msa.mpldraw.draw_loads(self.joints, self.members)
        self.canvas.show()

    def exec_msa(self):
        """Busca entre los perfiles disponibles el primero que
        cumpla el criterio de rigidez
        """
        self.save_and_reload_if_changed()
        msa.ui.info(">> Dimensionando los perfiles de la estructura... ")
        msa.search(self.joints, self.members, self.sections)
        #---
        file = open(self.filename, "r")
        rows = file.readlines()
        file.close()
        #---
        content = ""
        n = 0
        for row in rows:
            values = row.replace(',', '.').split(';')
            if re.search('^B\d+', values[0]):
                #XXX:que pasa aqui?
                type = values[4]
                type = self.members[n].type
                n = n + 1
            content += ";".join(values)
        #---
        #self.text.delete('1.0', tk.END)
        #self.text.insert('1.0', content)

    def solve_msa(self):
        """Resuelve la estructura por el metodo de la rigidez"""
        self.save_and_reload_if_changed()
        t0 = time.clock()
        msa.ui.info(">> Resolviendo estructura por el método de la rigidez... ")
        msa.solve(self.joints, self.members, self.sections)
        t1 = time.clock()
        msa.ui.info(">> Guardando los resultados... ")
        msa.htmlreport(self.joints, self.members)
        t2 = time.clock()
        msa.ui.warning(">> La estructura se ha resuelto en"
                       " %.2f segundos: %.2f calculo y %.2f dibujo "
                       % (t2-t0, t1-t0, t2-t1))
        webbrowser.open(os.path.join('output', 'report.html'))

def run():
    window = tk.Tk()
    window.title("MSA")
    window.geometry("+%d+%d" %(15, 15))
    #window.iconbitmap(os.path.join('icons', 'msa.ico'))
    Gui(window)
    window.mainloop()

if __name__ == "__main__":
    run()