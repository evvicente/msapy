# -*- coding: latin-1 -*-
__author__="Jorge Rodríguez Araújo"
__date__ ="$11-jul-2009 21:41:52$"

from pylab import *

import Tkinter as tk
import tkFileDialog
import tkMessageBox

from joint import *
from member import *

import msa2d
import draw2d

import os

class Gui():
    def __init__(self, window):
        self.window = window
        self.joints = []
        self.members = []
        
        self.filename = "input.csv"

        # Menú
        frame = tk.Frame(window)
        frame.pack(fill=tk.X, padx=3, pady=3)
        button = tk.Button(frame, text=" Open File... ", bg='lightgray', command=self.open_file)
        button.pack(side=tk.LEFT)
        button = tk.Button(frame, text=" Save As... ", bg='lightgray', command=self.save_file)
        button.pack(side=tk.LEFT)
        button = tk.Button(frame, text=" MSA ", fg='darkorange', bg='lightgray', command=lambda:tkMessageBox.showinfo("About", "MSA is a Python implementation of direct Matrix Stiffness Method for static structural analysis.\nAuthor: Jorge Rodríguez Araújo <grrodri@gmail.com>"), relief=tk.GROOVE)
        button.pack(side=tk.RIGHT)

        # Editor
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH)
        scrollbar = tk.Scrollbar(frame)
        self.text = tk.Text(frame, fg='black', bg='lightyellow', font="Courier 10")
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH)
        
        self.open_file(name = self.filename)

        # Solver
        frame = tk.Frame(window)
        frame.pack(fill=tk.X, padx=5, pady=5)
        button = tk.Button(frame, text=" SCHEMATIC ", fg='darkblue', command=self.draw_schematic)
        button.pack(side=tk.LEFT)
        button = tk.Button(frame, text=" SOLVE ", fg='darkred', command=self.solveMSA)
        button.pack(side=tk.LEFT)
        button = tk.Button(frame, text=" EXCEL ", fg='darkgreen', command=lambda:os.startfile("input.xls"))
        button.pack(side=tk.RIGHT)

        frame = tk.Frame(window)
        frame.pack(fill=tk.X)
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

        self.statusbar = tk.Label(frame, text="", bd=1, fg='white', relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=3, pady=3)
        self.statusbar['text'] = "Pulsa SCHEMATIC para representar la estructura"
        self.statusbar['background'] = 'darkblue'
    
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
        except:
            pass
    
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

        self.statusbar['text'] = "Pulsa SOLVE para resolver la estructura"
        self.statusbar['background'] = 'darkred'

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

    def solveMSA(self):
        self.statusbar['text'] = "Guardando los datos de definición de la estructura..."
        self.save_file(self.filename)
        self.statusbar['text'] = "Leyendo los datos de definición de la estructura..."
        (self.joints, self.members) = msa2d.load(self.filename)
        self.statusbar['text'] = "Resolviendo la estructura por el método de la rigidez..."
        msa2d.msa(self.joints, self.members)
        self.statusbar['text'] = "Guardando los resultados..."
        msa2d.save(self.joints, self.members)
        self.statusbar['text'] = "La estructura se ha resuelto con éxito"
        self.statusbar['background'] = 'darkgreen'
        self.draw_moments()

def run():
    window = tk.Tk()
    window.title("MSA")
    Gui(window)
    window.mainloop()

if __name__ == "__main__":
    run()