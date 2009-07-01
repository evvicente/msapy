# -*- coding: latin-1 -*-
__author__="Jorge"
__date__ ="$26-jun-2009 15:31:23$"

from pylab import *

class Joint():
    def __init__(self, X, Y, FX, FY, MZ, type = "rj"):
        """ Define un nudo de la estructura a partir de sus coordenadas y tipo """

        # Nudos (N): [X, Y]
        #   X = Coordenada horizontal en el eje de referencia absoluto
        #   Y = Coordenada vertical en el eje de referencia absoluto
        self.X = X
        self.Y = Y
        self.type = type # type: {fs, hs, rs, rj, hj}
    # Cargas en los nudos (lN): [FX, FY, MZ]
    #   FX = Carga según el eje horizontal
    #   FY = Carga según el eje vertical
    #   MZ = Momento según el eje Z
        self.__load = [FX, FY, MZ]

    def setLoad(self, FX, FY, MZ):
        """ Establece las cargas en el nudo:
           FX = Carga en el nudo según el eje X
           FY = Carga en el nudo según el eje Y
           MZ = Momento en el nudo según el eje Z """

        self.__load = [FX, FY, MZ]

    def getLoad(self):
        return self.__load

    def draw(self):
        """ Representa el nudo o apoyo """

        if self.type == "fs": # fixed support
            t = "$\\bot$\n"
        elif self.type == "hs": # hinge support
            t = "$\\bigtriangleup$\n"
        elif self.type == "rs": # roller support
            t = "$\\triangleq$\n"
        elif self.type == "hj": # hinge joint
            t = "\n"
        else: # rigid joint
            t = "\n"
        text(self.X, self.Y, t, verticalalignment='top', horizontalalignment='center', fontsize=18, color='black')

    def drawLoads(self):
        """ Dibuja las cargas sobre el nudo """

        t = ""
        if self.__load[0] > 0:
            t = "$\\rightarrow$"
        elif self.__load[0] < 0:
            t = "$\\leftarrow$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.__load[1] > 0:
            t = "$\uparrow$"
        elif self.__load[1] < 0:
            t = "$\downarrow$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.__load[2] > 0:
            t = "$\circlearrowleft$"
        elif self.__load[2] < 0:
            t = "$\circlearrowright$"
        text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if self.__load != [0,0,0]:
            t = ""
            if self.__load[0] != 0:
                t += "$N = %.2f$\n" %abs(self.__load[0])
            if self.__load[1] != 0:
                t += "$P_y = %d$\n" %abs(self.__load[1])
            if self.__load[2] != 0:
                t += "$M = %.2f$\n" %abs(self.__load[2])
            text(self.X, self.Y, t, verticalalignment='bottom', horizontalalignment='center', color='red')
 
if __name__ == "__main__":
    joint = Joint(0.1, 0.5, "rs")
    joint.setLoad(10, 10, 10)
    joint.draw()
    joint.drawLoads(3)
    show()
    