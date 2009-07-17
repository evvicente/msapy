# -*- coding: latin-1 -*-
__author__="Jorge Rodríguez Araújo"
__date__ ="$11-jul-2009 21:41:52$"

from pylab import *

import Tkinter as tk
import tkFileDialog

import io
from joint import *
from member import *

import msa2d

import os

class Gui():
    def __init__(self, window):
        menubar = tk.Menu(window)
        fileMenu = tk.Menu(menubar, tearoff=0)
        helpMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open File...", command=self.loadFile)
        fileMenu.add_command(label="Save As...", command=self.save)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=window.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        window.config(menu=menubar)

        self.text = tk.Text(window, fg="orange", font="Courier 10", height=15)
        self.text.pack(fill=tk.BOTH, padx=1, pady=1)
        self.filename = "input.csv"
        file = open(self.filename, "r")
        contents = file.read()
        file.close()
        window.title("MSA - " + self.filename)
        self.text.insert(tk.CURRENT, contents)

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, padx=5, pady=5)

        buttonTemplate = tk.Button(frame, text="EXCEL", command=lambda:os.startfile("template.xls"))
        buttonTemplate.pack(side=tk.RIGHT)
        
        buttonSchematic = tk.Button(frame, text="Schematic", command=self.draw_schematic)
        buttonSchematic.pack(side=tk.LEFT)

        buttonSolve = tk.Button(frame, text="SOLVE", command=self.solveMSA)
        buttonSolve.pack(side=tk.LEFT)

        buttonDisplacements = tk.Button(window, text="D", command=self.draw_displacements)
        buttonDisplacements.pack(side=tk.RIGHT)
        buttonMoments = tk.Button(window, text="M", command=self.draw_moments)
        buttonMoments.pack(side=tk.RIGHT)
        buttonShears = tk.Button(window, text="V", command=self.draw_shears)
        buttonShears.pack(side=tk.RIGHT)
        buttonNormals = tk.Button(window, text="N", command=self.draw_normals)
        buttonNormals.pack(side=tk.RIGHT)
        buttonReactions = tk.Button(window, text="R", command=self.draw_reactions)
        buttonReactions.pack(side=tk.RIGHT)

        self.statusbar = tk.Label(window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.joints = []
        self.members = []
        
    def loadFile(self):
        file = tkFileDialog.askopenfile(mode='r')
        try:
            contents = file.read()
            self.text.delete(tk.CURRENT, tk.END)
            self.text.insert(tk.CURRENT, contents)
        except:
            pass
    
    def save(self):
        file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
        saveFile(file)
    
    def saveFile(self, file):
        try:
            contents = str(self.text.get(0.0, tk.END))
            file.write(contents)
            file.close()
        except:
            pass

    def draw_schematic(self):
        file = open(self.filename, "w")
        contents = str(self.text.get(0.0, tk.END))
        file.write(contents)
        file.close()
        
        (self.joints, self.members) = io.load(self.filename)
        fig = figure(1)
        fig.clear()
        io.draw_schematic(self.joints, self.members)
        fig.show()

    def draw_reactions(self):
        fig = figure(1)
        fig.clear()
        io.draw_reactions(self.joints, self.members)
        fig.show()

    def draw_normals(self):
        fig = figure(1)
        fig.clear()
        io.draw_normals(self.members)
        fig.show()

    def draw_shears(self):
        fig = figure(1)
        fig.clear()
        io.draw_shears(self.members)
        fig.show()

    def draw_moments(self):
        fig = figure(1)
        fig.clear()
        io.draw_moments(self.members)
        fig.show()

    def draw_displacements(self):
        fig = figure(1)
        fig.clear()
        io.draw_displacements(self.joints, self.members)
        fig.show()

    def solveMSA(self):
        self.statusbar['text'] = "Guardando los datos de definición de la estructura..."
        self.saveFile(open(self.filename, 'w'))
        self.statusbar['text'] = "Leyendo los datos de definición de la estructura..."
        (self.joints, self.members) = io.load(self.filename)
        self.statusbar['text'] = "Resolviendo la estructura por el método de la rigidez..."
        msa2d.msa(self.joints, self.members)
        self.statusbar['text'] = "Guardando los resultados..."
        io.save(self.joints, self.members, self.filename)
        self.statusbar['text'] = "La estructura ha sido resuelta con éxito!"
        self.draw_moments()

def run():
    window = tk.Tk()
    window.title("MSA")
    Gui(window)
    window.mainloop()

if __name__ == "__main__":
    run()