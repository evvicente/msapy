# -*- coding: latin-1 -*-
__author__="Jorge Rodríguez Araújo"
__date__ ="$26-jun-2009 15:31:23$"

from pylab import *

class Member():
    def __init__(self, i, j, X1, Y1, X2, Y2, E, A, I, qy = 0):
        """ Define un miembro estructural a partir de sus coordenadas y propieades """
    
        self.i = i # Nudo inicial de la barra
        self.j = j # Nudo final de la barra
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2
        self.E = E # Módulo de elasticidad
        self.A = A # Area de la sección de la barra
        self.I = I # Momento de inercia de la sección
        self.qx = 0
        self.qy = qy # Carga uniformemente distribuida

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

        self.N1 = 0
        self.V1 = 0
        self.M1 = 0
        self.N2 = 0
        self.V2 = 0
        self.M2 = 0
        
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

    def setEfforts(self, N1, V1, M1, N2, V2, M2):
        (self.N1, self.V1, self.M1, self.N2, self.V2, self.M2) = (N1, V1, M1, N2, V2, M2)

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
        plot([self.X1, self.X2], [self.Y1, self.Y2], color='gray', lw=2)

    def __getCos(self):
        cos = (self.X2 - self.X1)/self.L
        return cos

    def __getSin(self):
        sin = (self.Y2 - self.Y1)/self.L
        return sin

    def drawLoads(self, scale = 0.0001):
        """ Dibuja las cargas sobre la barra """
        if self.qy != 0:
            s = self.__getSin()
            c = self.__getCos()
            XL1 = self.X1 - scale * abs(self.qy) * s
            XL2 = self.X2 - scale * abs(self.qy) * s
            YL1 = self.Y1 + scale * abs(self.qy) * c
            YL2 = self.Y2 + scale * abs(self.qy) * c
            fill([self.X1, XL1, XL2, self.X2], [self.Y1, YL1, YL2, self.Y2], hatch='|', facecolor='black')

            txt = "$q_y = %d$" %self.qy
            text((self.X1 + self.X2 + XL1 + XL2)/4, (self.Y1 + self.Y2 + YL1 + YL2)/4, txt, verticalalignment='center', horizontalalignment='center', color='red')

    def drawNormal(self, scale=0.001):
        """ Dibuja el diagrama de esfuerzos normales """
        
        s = self.__getSin()
        c = self.__getCos()
        XN1 = self.X1 + scale * self.N1 * s
        YN1 = self.Y1 - scale * self.N1 * c
        XN2 = self.X2 - scale * self.N2 * s
        YN2 = self.Y2 + scale * self.N2 * c
        # Escribe el valor del esfuerzo normal
        txt = "%.4f\n" %self.N2
        text((self.X1 + self.X2)/2, (self.Y1 + self.Y2)/2, txt, verticalalignment='center', horizontalalignment='center', fontsize=9, color='black')
        # Dibuja el diagrama
        fill([self.X1, XN1, XN2, self.X2], [self.Y1, YN1, YN2, self.Y2], facecolor='red')

    def drawShear(self, scale=0.0001):
        """ Dibuja el diagrama de esfuerzos cortantes """
        
        s = self.__getSin()
        c = self.__getCos()
        # Dibuja el diagrama
        V = 0
        if self.qy == 0:
            x = arange(0, 1.1, 0.5)
            x = x * self.L
            V = - self.V1
        else:
            x = arange(0, 1.1, 0.5)
            x = x * self.L
            V = - self.V1 - self.qy * x
        X = x * c + self.X1
        Y = x * s + self.Y1
        X = X - (scale * s * V)
        Y = Y + (scale * c * V)
        X = [self.X1] + list(X) + [self.X2]
        Y = [self.Y1] + list(Y) + [self.Y2]
        fill(X, Y, facecolor='green')
        # Escribe los valores de los esfuerzos cortantes
        txt = "\n\n%.4f\n" %abs(self.V1)
        if self.V1 > 0:
            text(X[1], Y[1], txt, verticalalignment='top', horizontalalignment='center', fontsize=9, color='black')
        else:
            text(X[1], Y[1], txt, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='black')
        txt = "\n\n%.4f\n" %abs(self.V2)
        if self.V2 > 0:
            text(X[-2], Y[-2], txt, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='black')
        else:
            text(X[-2], Y[-2], txt, verticalalignment='top', horizontalalignment='center', fontsize=9, color='black')

    def drawMoment(self, scale=0.0001):
        """ Dibuja el diagrama de momentos flectores """

        s = self.__getSin()
        c = self.__getCos()
        # Dibuja el diagrama
        M = 0
        if self.qy == 0:
            x = arange(0, 1.1, 0.5)
            x = x * self.L
            M = - self.M1 + (self.V1 * x)
        else:
            x = arange(0, 1.1, 0.1)
            x = x * self.L
            M = - self.M1 + (self.V1 * x) + (self.qy * x * x/2)
            # Momento máximo (x = - V1/qy)
            xmax = - self.V1 / self.qy
            Mmax = - self.M1 - ((self.V1 * self.V1) / (2 * self.qy))
            txt = "\n x = %.4f\n Mmax = %.4f\n\n\n" %(xmax, Mmax)
            text((self.X1 + self.X2)/2, (self.Y1 + self.Y2)/2, txt, verticalalignment='center', horizontalalignment='center', fontsize=9, color='red')

        X = x * c + self.X1
        Y = x * s + self.Y1
        X = X + (scale * s * M)
        Y = Y - (scale * c * M)
        X = [self.X1] + list(X) + [self.X2]
        Y = [self.Y1] + list(Y) + [self.Y2]
        fill(X, Y, facecolor='blue')
        # Escribe los valores de los momentos en extremo de barra
        txt = "\n\n%.4f\n" %abs(self.M1)
        if self.M1 > 0:
            text(X[1], Y[1], txt, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='black')
        else:
            text(X[1], Y[1], txt, verticalalignment='top', horizontalalignment='center', fontsize=9, color='black')
        txt = "\n\n%.4f\n" %abs(self.M2)
        if self.M2 > 0:
            text(X[-2], Y[-2], txt, verticalalignment='top', horizontalalignment='center', fontsize=9, color='black')
        else:
            text(X[-2], Y[-2], txt, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='black')

if __name__ == "__main__":
    member = Member(0, 1, 0, 0, 1, 0.5, 21000, 0.01, 100)
    member.setUniform(150)
    axis('equal')
    member.draw()
    member.drawLoads()
    member.drawNormal(100, -100)
    member.drawShear(100, -100)
    member.drawMoment(100, -100, 1000, 0)
    show()
    