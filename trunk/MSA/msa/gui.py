#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Tkinter as tk
import tkFileDialog

from joint2d import *
from member2d import *

import io
import msa2d
import draw2d

import os
import time
import webbrowser

class Gui():
    def __init__(self, window):
        self.window = window
        self.joints = []
        self.members = []
        self.filename = "input.csv"

        # Menu
        menu_frame = tk.Frame(window)
        menu_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=3, pady=2)
        # Open file
        img = tk.PhotoImage(file='icons/open.gif')
        button = tk.Button(menu_frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.open_file)
        button.image = img
        button.pack(side='left')
        # Save file
        img = tk.PhotoImage(file='icons/save.gif')
        button = tk.Button(menu_frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.save_file)
        button.image = img
        button.pack(side='left', padx=5)
        # Help
        img = tk.PhotoImage(file='icons/help.gif')
        button = tk.Button(menu_frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:webbrowser.open(os.path.join('help', 'index.html')))
        button.image = img
        button.pack(side='right')
        # Template
        img = tk.PhotoImage(file='icons/excel.gif')
        button = tk.Button(menu_frame, image=img, text="        ", compound='center', relief=tk.GROOVE, command=lambda:os.system('input.xls'))
        button.image = img
        button.pack(side='right', padx=10)

        # PLot
        self.plot_frame = tk.Frame(window)
        self.plot_frame.grid(row=1, column=0)
        self.fig = figure(1, figsize=(8.14, 4.73))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill='both', expand='yes')

        # Text
        self.text_frame = tk.Frame(window)
        self.text_frame.grid(row=1, column=0)
        scrollbar = tk.Scrollbar(self.text_frame)
        self.text = tk.Text(self.text_frame, fg='darkorange', bg='#FAFAFA', font="Courier 10")
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill=tk.Y)
        self.text.pack(fill='both', expand='yes')
        
        # Tools
        tools_frame = tk.Frame(window)
        tools_frame.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=3, pady=4)
        # Show editor
        img = tk.PhotoImage(file='icons/editor.gif')
        button = tk.Button(tools_frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.show_editor)
        button.image = img
        button.pack(side='left')
        # Show schematic
        img = tk.PhotoImage(file='icons/schematic.gif')
        button = tk.Button(tools_frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.show_schematic)
        button.image = img
        button.pack(side='left', padx=5)
        # Solver
        img = tk.PhotoImage(file='icons/solve.gif')
        button = tk.Button(tools_frame, image=img, text="      ", compound='center', bg='gray', relief=tk.GROOVE, command=self.solve_msa)
        button.image = img
        button.pack(side='left', padx=5)
        # Exit
        img = tk.PhotoImage(file='icons/exit.gif')
        button = tk.Button(tools_frame, image=img, text="     ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:self.window.quit())
        button.image = img
        button.pack(side='right')
        # Status bar
        self.statusbar = tk.Label(tools_frame, text=" MSA - Copyright 2009 Jorge Rodríguez Araújo ", bd=1, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, expand='yes')

        # Open default file
        self.open_file(name = self.filename)
    
    def open_file(self, name=""):
        """ Abre un archivo """
        if name == "":
            file = tkFileDialog.askopenfile(mode='r')
        else:
            file = open(name, "r")
        try:
            contents = file.read()
            self.text.delete(tk.CURRENT, tk.END)
            self.text.insert(tk.CURRENT, contents)
            self.filename = file.name
            self.window.title("MSA - " + self.filename)
            self.statusbar['text'] = " El archivo se ha cargado con éxito "
        except:
            self.statusbar['text'] = " No se ha podido abrir el archivo "
    
    def save_file(self, name=""):
        """ Guarda un archivo """
        if name == "":
            file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
        else:
            file = open(name, "w")
        try:
            contents = str(self.text.get(0.0, tk.END)).strip('\n')
            file.write(contents)
            file.close()
        except:
            pass

    def show_editor(self):
        """ Muestra el editor de texto """
        self.plot_frame.lower()
        self.text_frame.lift()

    def show_schematic(self):
        """ Guarda los datos y muestra el esquema estructural """
        self.text_frame.lower()
        self.plot_frame.lift()
        
        self.save_file(name = self.filename)
        
        (self.joints, self.members, properties) = io.load(self.filename)

        self.fig.clear()
        draw2d.show_schematic(self.joints, self.members)
        draw2d.draw_loads(self.joints, self.members)
        self.canvas.show()
        
        self.statusbar['text'] = ""

    def solve_msa(self):
        t0 = time.clock()
        self.statusbar['text'] = " Guardando los datos de definición de la estructura... "
        self.save_file(self.filename)
        self.statusbar['text'] = " Leyendo los datos de definición de la estructura... "
        (self.joints, self.members, properties) = io.load(self.filename)
        self.statusbar['text'] = " Resolviendo la estructura por el método de la rigidez... "
        msa2d.msa(self.joints, self.members, properties)
        t1 = time.clock()
        self.statusbar['text'] = " Guardando los resultados... "
        io.report(self.joints, self.members)
        t2 = time.clock()
        self.statusbar['text'] = " La estructura se ha resuelto en %.2f segundos: %.2f calculo y %.2f dibujo " %(t2-t0, t1-t0, t2-t1)
        webbrowser.open(os.path.join('output', 'report.html'))

def run():
    window = tk.Tk()
    window.title("MSA")
    window.geometry("+%d+%d" %(5, 5))
    #window.iconbitmap(os.path.join('icons', 'msa.ico'))
    Gui(window)
    window.mainloop()

if __name__ == "__main__":
    run()
