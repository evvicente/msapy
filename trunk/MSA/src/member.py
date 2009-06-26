# -*- coding: latin-1 -*-
__author__="Jorge"
__date__ ="$26-jun-2009 15:31:23$"

from pylab import *

class Member():
    def __init__(self, i, j, X1, Y1, X2, Y2, E, A, I, qy = 0):
        """ Define un miembro estructural a partir de sus coordenadas y propieades """

    # Barras (B): [i, j, E, A, Iz]
    #   i = Nudo inicial de la barra
    #   j = Nudo final de la barra
    #   E = Módulo de elasticidad
    #   A = Area de la sección de la barra
    #   I = Momento de inercia de la sección
    #   q = Carga uniformemente distribuida
        self.i = i
        self.j = j
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2
        self.E = E
        self.A = A
        self.I = I
        self.qx = 0
        self.qy = qy
    # Definición de las cargas
    #----------------------------------------------------------
    # Cargas en los extremos de las barras (lB): [Fxi, Fyi, Mzi, Fxj, Fyj, Mzj]
    #   Fxi = Carga en el nudo i según el eje x de la barra
    #   Fyi = Carga en el nudo i según el eje y de la barra
    #   Mzi = Momento en el nudo i según el eje z de la barra
    #   Fxj = Carga en el nudo j según el eje x de la barra
    #   Fyj = Carga en el nudo j según el eje y de la barra
    #   Mzj = Momento en el nudo j según el eje z de la barra
        self.__load = [0, 0, 0, 0, 0, 0]
        
        self.L = self.getLength()
        self.qy = qy
        if qy != 0:
            self.setUniform(qy)
        
    # Longitud de la barra
    def getLength(self):
        """ Calcula la longitud de la barra """

        L = sqrt((self.X2 - self.X1)**2 + (self.Y2 - self.Y1)**2)

        return L

    def setLoad(self, Fxi, Fyi, Mzi, Fxj, Fyj, Mzj):
        """ Establece las cargas en los extremos de la barra:
           Fxi = Carga en el nudo i según el eje x de la barra
           Fyi = Carga en el nudo i según el eje y de la barra
           Mzi = Momento en el nudo i según el eje z de la barra
           Fxj = Carga en el nudo j según el eje x de la barra
           Fyj = Carga en el nudo j según el eje y de la barra
           Mzj = Momento en el nudo j según el eje z de la barra """

        self.__load = [Fxi, Fyi, Mzi, Fxj, Fyj, Mzj]

    def getLoad(self):
        return self.__load

    # Carga uniforme
    def setUniform(self, qy):
        """ Calcula las reacciones de empotramiento perfecto para una carga
        uniformente repartida en toda la barra. """

        self.qy = qy

        V = - qy * self.L / 2
        M = qy * self.L**2 / 12

        self.__load = [0, V, -M, 0, V, M]

    def draw(self):
        """ Dibuja la barra """

        plot([self.X1, self.X2], [self.Y1, self.Y2], color='gray', linewidth=1.5)

    def __getCos(self):
        cos = (self.X2 - self.X1)/self.L
        return cos

    def __getSin(self):
        sin = (self.Y2 - self.Y1)/self.L
        return sin

    def drawLoads(self):
        """ Dibuja las cargas sobre la barra """
        if self.qy != 0:
            s = self.__getSin()
            c = self.__getCos()
            fill([self.X1, self.X1-0.01*self.qy*s, self.X2-0.01*self.qy*s, self.X2], [self.Y1, self.Y1+0.01*self.qy*c, self.Y2+0.01*self.qy*c, self.Y2], facecolor='red')

        """ t = ":\n :\n L%d:\n" %n
            t += "%f   $N$   %f\n" %(lB[n][0], lB[n][3])
            t += "%f   $V$   %f\n" %(lB[n][1], lB[n][4])
            t += "%f   $M$   %f\n" %(lB[n][2], lB[n][5])
            text((X1+X2)/2, (Y1+Y2)/2, t, verticalalignment='top', horizontalalignment='center', fontsize=9, color='red')"""

if __name__ == "__main__":
    member = Member(0, 1, 0, 0, 1, 0, 21000, 0.01, 100)
    member.setUniform(15)
    member.draw()
    member.drawLoads()
    show()
    