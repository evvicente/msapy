# -*- coding: latin-1 -*-
__author__="Jorge Rodríguez Araújo"
__date__ ="$26-jun-2009 15:31:23$"

from pylab import *

class Joint():
    def __init__(self, X, Y, FX, FY, MZ, type = "rj"):
        """ Define un nudo de la estructura a partir de sus coordenadas y tipo """

        # Coordenadas en el eje de referencia absoluto
        self.X = X # Horizontal
        self.Y = Y # Vertical

        # Tipo de nudo o apoyo
        self.type = type # type: {fs, hs, rs, rj, hj}

        # Cargas en el nudo
        self.FX = FX
        self.FY = FY
        self.MZ = MZ

        # Desplazamientos y giro
        self.dX = 0
        self.dY = 0
        self.gZ = 0

        # Reacciones
        self.RX = 0
        self.RY = 0
        self.RMZ = 0

    def setLoad(self, FX, FY, MZ):
        """ Establece las cargas en el nudo:
            FX = Carga según el eje X
            FY = Carga según el eje Y
            MZ = Momento según el eje Z """

        (self.FX, self.FY, self.MZ) = (FX, FY, MZ)

    def getLoad(self):
        return [self.FX, self.FY, self.MZ]

    def setDisplacements(self, dX, dY, gZ):
        """ Establece los desplazamientos del nudo:
            dX = Desplazamiento según el eje X
            dY = Desplazamiento según el eje Y
            gZ = Giro según el eje Z """

        (self.dX, self.dY, self.gZ) = (dX, dY, gZ)

    def setReactions(self, RX, RY, RMZ):
        """ Establece las reacciones del apoyo:
            RX = Reacción según el eje X
            RY = Reacción según el eje Y
            RMZ = Momento según el eje Z """

        (self.RX, self.RY, self.RMZ) = (RX, RY, RMZ)
        
    def draw(self):
        """ Representa el nudo o apoyo """
        
        if self.type == "hj": # hinge joint
            text(self.X, self.Y, "o", verticalalignment='center', horizontalalignment='center', fontsize=9, color='black')
        elif self.type == "fs": # fixed support
            text(self.X, self.Y, "$\\bot$\n", verticalalignment='top', horizontalalignment='center', fontsize=18, color='black')
        elif self.type == "hs": # hinge support
            text(self.X, self.Y, "$\\bigtriangleup$\n", verticalalignment='top', horizontalalignment='center', fontsize=18, color='black')
        elif self.type == "rs": # roller support
            text(self.X, self.Y, "$\\triangleq$\n", verticalalignment='top', horizontalalignment='center', fontsize=18, color='black')

    def draw_loads(self):
        """ Dibuja las cargas sobre el nudo """

        t = ""
        if self.FX > 0:
            t = "$\\rightarrow$"
        elif self.FX < 0:
            t = "$\\leftarrow$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.FY > 0:
            t = "$\uparrow$"
        elif self.FY < 0:
            t = "$\downarrow$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.MZ > 0:
            t = "$\circlearrowleft$"
        elif self.MZ < 0:
            t = "$\circlearrowright$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.getLoad() != [0,0,0]:
            t = ""
            if self.FX != 0:
                t += "$N = %.2f$\n" %abs(self.FX)
            if self.FY != 0:
                t += "$P_y = %d$\n" %abs(self.FY)
            if self.MZ != 0:
                t += "$M = %.2f$\n" %abs(self.MZ)
            text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', color='red')
    
    def draw_reactions(self):
        """ Dibuja las reacciones en los apoyos """

        if self.RX > 0.001:
            txt = "\n\n$\\rightarrow$\n %.2f\n" %self.RX
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='red')
        elif self.RX < 0:
            txt = "\n\n$\\leftarrow$\n %.2f\n" %abs(self.RX)
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='red')
        if self.RY > 0.001:
            txt = "\n\n$\\uparrow$\n %.2f\n" %self.RY
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='green')
        elif self.RY < 0:
            txt = "\n\n$\\downarrow$\n %.2f\n" %abs(self.RY)
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='green')
        if self.RMZ > 0.001:
            txt = "\n\n$\\circlearrowleft$\n %.2f\n" %self.RMZ
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='blue')
        elif self.RMZ < 0:
            txt = "\n\n$\\circlearrowright$\n %.2f\n" %abs(self.RMZ)
            text(self.X, self.Y, txt, verticalalignment='top', horizontalalignment='center', fontsize=15, color='blue')

