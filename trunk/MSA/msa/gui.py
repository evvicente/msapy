#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylab import *

import Tkinter as tk
import tkFileDialog

from joint2d import *
from member2d import *

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
        frame = tk.Frame(window)
        frame.pack(fill=tk.X, padx=3, pady=3)
        # Open file
        img = tk.PhotoImage(file='icons/open.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.open_file)
        button.image = img
        button.pack(side='left')
        # Save file
        img = tk.PhotoImage(file='icons/save.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.save_file)
        button.image = img
        button.pack(side='left', padx=5)
        # Help
        img = tk.PhotoImage(file='icons/help.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:webbrowser.open(os.path.join('help', 'index.html')))
        button.image = img
        button.pack(side='right')
        # Template
        img = tk.PhotoImage(file='icons/excel.gif')
        button = tk.Button(frame, image=img, text="        ", compound='center', relief=tk.GROOVE, command=lambda:os.system('input.xls'))
        button.image = img
        button.pack(side='right', padx=10)

        # Editor
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand='yes')
        scrollbar = tk.Scrollbar(frame)
        self.text = tk.Text(frame, fg='darkorange', bg='#FAFAFA', font="Courier 10")
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand='yes')

        # Tools
        frame = tk.Frame(window)
        frame.pack(fill=tk.X, pady=5)
        # Draw
        img = tk.PhotoImage(file='icons/refresh.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.draw_schematic)
        button.image = img
        button.pack(side='left', padx=5)
        # Solver
        img = tk.PhotoImage(file='icons/solve.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.solve_msa)
        button.image = img
        button.pack(side='left')
        # Exit
        img = tk.PhotoImage(file='icons/exit.gif')
        button = tk.Button(frame, image=img, text="          ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:self.window.quit())
        button.image = img
        button.pack(side='right', padx=5)
        # Status bar
        self.statusbar = tk.Label(frame, text=" MSA - Copyright 2009 Jorge Rodríguez Araújo ", bd=1, anchor=tk.W)
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

    def draw_schematic(self):
        self.save_file(name = self.filename)
        
        (self.joints, self.members) = msa2d.load(self.filename)
        fig = figure(1)
        fig.clear()
        draw2d.draw_schematic(self.joints, self.members)
        draw2d.draw_loads(self.joints, self.members)
        fig.show()
        
        self.statusbar['text'] = ""

    def solve_msa(self):
        t0 = time.clock()
        self.statusbar['text'] = " Guardando los datos de definición de la estructura... "
        self.save_file(self.filename)
        self.statusbar['text'] = " Leyendo los datos de definición de la estructura... "
        (self.joints, self.members, properties) = msa2d.load(self.filename)
        self.statusbar['text'] = " Resolviendo la estructura por el método de la rigidez... "
        msa2d.msa(self.joints, self.members, properties)
        t1 = time.clock()
        self.statusbar['text'] = " Guardando los resultados... "
        draw2d.report(self.joints, self.members)
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
