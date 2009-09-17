# -*- coding: latin-1 -*-
__author__="Jorge Rodr�guez Ara�jo"
__date__ ="$11-jul-2009 21:41:52$"

from pylab import *

import Tkinter as tk
import tkFileDialog

from joint2d import *
from member2d import *

import msa2d
import draw2d

import os
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
        button.pack(side='left')
        # Help
        img = tk.PhotoImage(file='icons/help.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:webbrowser.open(os.path.join('help', 'index.html')))
        button.image = img
        button.pack(side='right')
        # Template
        img = tk.PhotoImage(file='icons/excel.gif')
        button = tk.Button(frame, image=img, text=" EXCEL ", compound='left', fg='darkgreen', relief=tk.GROOVE, command=lambda:os.system('input.xls'))
        button.image = img
        button.pack(side='right', padx=10)

        # Editor
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand='yes')
        scrollbar = tk.Scrollbar(frame)
        self.text = tk.Text(frame, fg='darkorange', bg='white', font="Courier 10")
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand='yes')

        # Tools
        frame = tk.Frame(window)
        frame.pack(fill=tk.X, padx=5, pady=5)
        # Refresh
        img = tk.PhotoImage(file='icons/refresh.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.draw_schematic)
        button.image = img
        button.pack(side='left')
        # Solver
        img = tk.PhotoImage(file='icons/solve.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=self.solve_msa)
        button.image = img
        button.pack(side='left')
        # Report
        img = tk.PhotoImage(file='icons/report.gif')
        button = tk.Button(frame, image=img, text=" ", compound='center', bg='gray', relief=tk.GROOVE, command=lambda:webbrowser.open(os.path.join('output', 'report.html')))
        button.image = img
        button.pack(side='left', padx=10)
        #button.pack_forget()
        # Graphics
        buttonDisplacements = tk.Button(frame, text=" D ", bg='gray', command=self.draw_displacements, relief=tk.GROOVE)
        buttonDisplacements.pack(side=tk.RIGHT)
        buttonMoments = tk.Button(frame, text=" M ", bg='gray', command=self.draw_moments, relief=tk.GROOVE)
        buttonMoments.pack(side=tk.RIGHT)
        buttonShears = tk.Button(frame, text=" V ", bg='gray', command=self.draw_shears, relief=tk.GROOVE)
        buttonShears.pack(side=tk.RIGHT)
        buttonNormals = tk.Button(frame, text=" N ", bg='gray', command=self.draw_normals, relief=tk.GROOVE)
        buttonNormals.pack(side=tk.RIGHT)
        buttonReactions = tk.Button(frame, text=" R ", bg='gray', command=self.draw_reactions, relief=tk.GROOVE)
        buttonReactions.pack(side=tk.RIGHT)
        # Status bar
        self.statusbar = tk.Label(frame, text="", bd=1, fg='white', relief=tk.GROOVE, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=3, pady=3)

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
            self.statusbar['text'] = ""
            self.statusbar['background'] = 'lightblue'
        except:
            self.statusbar['text'] = "Warning! No se ha podido abrir el archivo."
            self.statusbar['background'] = 'red'
    
    def save_file(self, name=""):
        """ Guarda un archivo """
        if name == "":
            file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
        else:
            file = open(name, "w")
        try:
            contents = str(self.text.get(0.0, tk.END))
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
        fig.show()
        
        self.statusbar['text'] = ""
        self.statusbar['background'] = 'darkgray'

    def draw_reactions(self):
        fig = figure(1)
        fig.clear()
        draw2d.draw_reactions(self.joints, self.members)
        fig.show()

    def draw_normals(self):
        fig = figure(1)
        fig.clear()
        draw2d.draw_normals(self.members)
        fig.show()

    def draw_shears(self):
        fig = figure(1)
        fig.clear()
        draw2d.draw_shears(self.members)
        fig.show()

    def draw_moments(self):
        fig = figure(1)
        fig.clear()
        draw2d.draw_moments(self.members)
        fig.show()

    def draw_displacements(self):
        fig = figure(1)
        fig.clear()
        draw2d.draw_displacements(self.joints, self.members)
        fig.show()

    def solve_msa(self):
        self.statusbar['text'] = "Guardando los datos de definici�n de la estructura..."
        self.save_file(self.filename)
        self.statusbar['text'] = "Leyendo los datos de definici�n de la estructura..."
        (self.joints, self.members) = msa2d.load(self.filename)
        self.statusbar['text'] = "Resolviendo la estructura por el m�todo de la rigidez..."
        msa2d.msa(self.joints, self.members)
        self.statusbar['text'] = "Guardando los resultados..."
        draw2d.report(self.joints, self.members)
        self.statusbar['text'] = "La estructura se ha resuelto con �xito"
        self.statusbar['background'] = 'lightblue'
        self.draw_moments()

def run():
    window = tk.Tk()
    window.title("MSA")
    #window.iconbitmap(os.path.join('icons', 'msa.ico'))
    Gui(window)
    window.mainloop()

if __name__ == "__main__":
    run()