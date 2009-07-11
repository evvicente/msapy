# -*- coding: latin-1 -*-
__author__="Jorge"
__date__ ="$11-jul-2009 21:41:52$"

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import Tkinter as tk

class Notebook():
	def __init__(self, master, side=tk.LEFT):
		self.active_fr = None
		self.count = 0
		self.choice = tk.IntVar(0)

		if side in (tk.TOP, tk.BOTTOM):
			self.side = tk.LEFT
		else:
			self.side = tk.TOP

		# creates notebook's frames structure
		self.rb_fr = tk.Frame(master, borderwidth=2, relief=tk.RIDGE)
		self.rb_fr.pack(side=side, fill=tk.BOTH)
		self.screen_fr = tk.Frame(master, borderwidth=2, relief=tk.RIDGE)
		self.screen_fr.pack(fill=tk.BOTH)

	# return a master frame reference for the external frames (screens)
	def __call__(self):
		return self.screen_fr

	# add a new frame (screen) to the (bottom/left of the) notebook
	def add_screen(self, fr, title):
		b = tk.Radiobutton(self.rb_fr, text=title, indicatoron=0, variable=self.choice, value=self.count, command=lambda: self.display(fr))
		b.pack(fill=tk.BOTH, side=self.side)

		# ensures the first frame will be
		# the first selected/enabled
		if not self.active_fr:
			fr.pack(fill=tk.BOTH, expand=1)
			self.active_fr = fr

		self.count += 1

		# returns a reference to the newly created
        # radiobutton (allowing its configuration/destruction)
                return b

	# hides the former active frame and shows
	# another one, keeping its reference
	def display(self, fr):
		self.active_fr.forget()
		fr.pack(fill=tk.BOTH, expand=1)
		self.active_fr = fr

import io
from joint import *
from member import *
from MSA import *

import os

def solveMSA():
    filename = "input.csv"
    print "Leyendo los datos de definición de la estructura..."
    (joints, members) = io.load(filename)
    print "Resolviendo la estructura por el método de la rigidez..."
    msa(joints, members)

def run():
    window = tk.Tk()
    window.wm_title("MSA")
    
    notebook = Notebook(window)

    # Frame1
    f1 = tk.Frame(notebook())
    labelFilename = tk.Label(f1, text="\n   La estructura se encuentra definida en el archivo:   \n")
    labelFilename.pack()
    entryFilename = tk.Entry(f1)
    entryFilename.insert(tk.INSERT, "input.csv")
    entryFilename.pack()
    # Abre la plantilla de excel para generar un nuevo estudio
    bDefine = tk.Button(f1, text="EXCEL", command=lambda:os.startfile("template.xls"))
    bDefine.pack()
    lSolve = tk.Label(f1, text="\n   Resuelve la estructura con 'SOLVE'   \n")
    lSolve.pack()
    bSolve = tk.Button(f1, text="SOLVE", command=solveMSA)
    bSolve.pack(fill=tk.BOTH, expand=1)
    label = tk.Label(f1, text="   ")
    label.pack()

    # Frame2
    f2 = tk.Frame(notebook())
    fig = Figure()
    canvas = FigureCanvasTkAgg(fig, master=f2)
    plt = fig.add_subplot(111)
    plt.set_title("Esquema estructural")
    plt.set_xlabel("X")
    plt.set_ylabel("Y")
    plt.set_aspect('equal')
    (joints, members) = io.load("input.csv")
    for n in range(len(members)):
        plt.plot([members[n].X1, members[n].X2], [members[n].Y1, members[n].Y2], color="gray")
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Frames
    notebook.add_screen(f1, "Datos")
    notebook.add_screen(f2, "Esquema")

    window.mainloop()

if __name__ == "__main__":
    run()