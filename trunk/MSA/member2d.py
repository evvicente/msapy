# -*- coding: UTF-8 -*-

from pylab import *

class Member():
    def __init__(self, i, j, X1, Y1, X2, Y2, qy = 0):
        """ Define un miembro estructural a partir de sus coordenadas """

        # Identificacion de los nudos inicial y final
        self.i = i # Nudo inicial de la barra
        self.j = j # Nudo final de la barra

        # Coordenadas de los extremos inicial y final
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2
        # Datos auxiliares
        self.L = sqrt( (self.X2 - self.X1)**2 + (self.Y2 - self.Y1)**2 ) # Longitud
        self.sin = (self.Y2 - self.Y1) / self.L # Seno
        self.cos = (self.X2 - self.X1) / self.L # Coseno

        # Propiedades de la barra
        self.E = 0 # Modulo de elasticidad
        self.A = 0 # Area de la seccion
        self.Iz = 0 # Momento de inercia de la seccion
        self.Wz = 0 # Modulo resistente

        # Cargas uniformemente distribuidas
        self.qx = 0
        self.qy = qy

        # Cargas en extremo de barra: inicial (1) y final (2)
        #   Fx = Carga en el extremo segun el eje x de la barra
        #   Fy = Carga en el extremo segun el eje y de la barra
        #   Mz = Momento en el extremo segun el eje z de la barra
        self.Fx1 = 0
        self.Fy1 = 0
        self.Mz1 = 0     
        self.Fx2 = 0
        self.Fy2 = 0
        self.Mz2 = 0

        self.__load = [0, 0, 0, 0, 0, 0]

        # Transformacion de la carga uniforme
        if qy != 0:
            self.set_uniform(qy)

        # Esfuerzos resultantes en extremo de barra
        self.N1 = 0
        self.V1 = 0
        self.M1 = 0
        self.N2 = 0
        self.V2 = 0
        self.M2 = 0

        # Matrices de la barra
        self.k = 0 # Matriz de rigidez
        self.r = 0 # Matriz de rotacion
    
    def get_rotation_matrix(self):
        """ Devuelve la matriz de rotación de la barra """
        return self.r

    def get_stiffness_matrix(self):
        """ Devuelve la matriz de rigidez de la barra """
        return self.k

    def set_properties(self, A, E, Iz, Wz):
        """ Establece las propiedades de la barra """
        self.A = A
        self.E = E
        self.Iz = Iz
        self.Wz = Wz

    def set_loads(self, Fx1, Fy1, Mz1, Fx2, Fy2, Mz2):
        """ Establece las cargas en los extremos inicial (1) y final (2) de la barra,
        siendo F las fuerzas y M los momentos """
        self.__load = [Fx1, Fy1, Mz1, Fx2, Fy2, Mz2]

    def get_loads(self):
        return self.__load

    def set_efforts(self, N1, V1, M1, N2, V2, M2):
        (self.N1, self.V1, self.M1, self.N2, self.V2, self.M2) = (N1, V1, M1, N2, V2, M2)

    # Carga uniforme
    def set_uniform(self, qy):
        """ Calcula las reacciones de empotramiento perfecto para una carga
        uniformente repartida en toda la barra. """
        self.qy = qy

        V = - qy * self.L / 2
        M = qy * self.L**2 / 12

        self.__load = [0, V, -M, 0, V, M]

    # Momentos
    def M(self, x):
        """ Calcula el momento en un punto """
        M = self.M1 - self.v1 * x - self.qy * x * x / 2
        return M
    
    # Deformada
    def y(self, x, gz1, dy1):
        """ Calcula la flecha en un punto """
        y = (-1 / (self.E * self.Iz)) * (self.M1 * x**2 / 2 - self.V1 * x**3 / 6 - self.qy * x**4 / 24) + gz1 * x + dy1
        return y

    def draw_member(self):
        """ Dibuja la barra """
        plot([self.X1, self.X2], [self.Y1, self.Y2], color='gray', lw=2)

    def draw_loads(self, scale):
        """ Dibuja las cargas sobre la barra """
        if self.qy != 0:
            s = self.sin
            c = self.cos
            XL1 = self.X1 - scale * abs(self.qy) * s
            XL2 = self.X2 - scale * abs(self.qy) * s
            YL1 = self.Y1 + scale * abs(self.qy) * c
            YL2 = self.Y2 + scale * abs(self.qy) * c
            fill([self.X1, XL1, XL2, self.X2], [self.Y1, YL1, YL2, self.Y2], hatch='|', facecolor='black')

            txt = "%d" %self.qy
            text((self.X1 + self.X2 + XL1 + XL2)/4, (self.Y1 + self.Y2 + YL1 + YL2)/4, txt, va='center', ha='center', color='red')

    def draw_normal(self, scale):
        """ Dibuja el diagrama de esfuerzos normales """
        XN1 = self.X1 + scale * self.N1 * self.sin
        YN1 = self.Y1 - scale * self.N1 * self.cos
        XN2 = self.X2 - scale * self.N2 * self.sin
        YN2 = self.Y2 + scale * self.N2 * self.cos
        fill([self.X1, XN1, XN2, self.X2], [self.Y1, YN1, YN2, self.Y2], facecolor='red')
        txt = "%.1f\n" %round(self.N2, 1)
        text((self.X1 + self.X2 + XN1 + XN2)/4, (self.Y1 + self.Y2 + YN1 + YN2)/4, txt, va='center', ha='center', fontsize=10, color='black')

    def draw_shear(self, scale):
        """ Dibuja el diagrama de esfuerzos cortantes """

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

        X = x * self.cos + self.X1
        Y = x * self.sin + self.Y1
        X = X - (scale * self.sin * V)
        Y = Y + (scale * self.cos * V)
        X = [self.X1] + list(X) + [self.X2]
        Y = [self.Y1] + list(Y) + [self.Y2]
        fill(X, Y, facecolor='green')
        # Escribe los valores de los esfuerzos cortantes
        txt = "\n\n  %.1f\n" %abs(round(self.V1, 1))
        if self.V1 > 0:
            text(X[1], Y[1], txt, verticalalignment='top', horizontalalignment='left', fontsize=9, color='black')
        else:
            text(X[1], Y[1], txt, verticalalignment='bottom', horizontalalignment='left', fontsize=9, color='black')
        txt = "\n\n%.1f  \n" %abs(round(self.V2, 1))
        if self.V2 > 0:
            text(X[-2], Y[-2], txt, verticalalignment='bottom', horizontalalignment='right', fontsize=9, color='black')
        else:
            text(X[-2], Y[-2], txt, verticalalignment='top', horizontalalignment='right', fontsize=9, color='black')

    def draw_moment(self, scale):
        """ Dibuja el diagrama de momentos flectores """

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
            # Momento m�ximo (x = - V1/qy)
            xmax = - self.V1 / self.qy
            Mmax = - self.M1 - ((self.V1 * self.V1) / (2 * self.qy))
            txt = "\n x = %.4f\n Mmax = %.4f\n\n\n" %(xmax, Mmax)
            text((self.X1 + self.X2)/2, (self.Y1 + self.Y2)/2, txt, verticalalignment='center', horizontalalignment='center', fontsize=9, color='red')

        X = x * self.cos + self.X1
        Y = x * self.sin + self.Y1
        X = X + (scale * self.sin * M)
        Y = Y - (scale * self.cos * M)
        X = [self.X1] + list(X) + [self.X2]
        Y = [self.Y1] + list(Y) + [self.Y2]
        fill(X, Y, facecolor='blue')
        # Escribe los valores de los momentos en extremo de barra
        txt = "\n\n  %.1f\n" %abs(round(self.M1, 1))
        if self.M1 > 0:
            text(X[1], Y[1], txt, va='bottom', ha='left', fontsize=9, color='black')
        else:
            text(X[1], Y[1], txt, va='top', ha='left', fontsize=9, color='black')
        txt = "\n\n%.1f  \n" %abs(round(self.M2, 1))
        if self.M2 > 0:
            text(X[-2], Y[-2], txt, va='top', ha='right', fontsize=9, color='black')
        elif self.M2 < 0:
            text(X[-2], Y[-2], txt, va='bottom', ha='right', fontsize=9, color='black')
