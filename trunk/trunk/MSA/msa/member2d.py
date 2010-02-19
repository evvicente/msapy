# -*- coding: UTF-8 -*-

from pylab import *

class Member():
    def __init__(self, i, j, X1, Y1, X2, Y2, qy = 0, qY = 0):
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
        self.P = 0 # Peso de la barra
        # Propiedades del material
        self.E = 0 # Modulo de elasticidad
        self.d = 0 # Densidad del material
        self.fyd = 0 # Resistencia ultima del material
        # Propiedades geométricas
        self.type = '' # Designacion
        self.A = 0 # Area de la seccion
        self.Iz = 0 # Momento de inercia de la seccion
        self.Wz = 0 # Modulo resistente
        
        # Cargas uniformemente distribuidas
        self.qx = 0
        self.qy = qy
        self.qY = qY # Peso

        # Esfuerzos resultantes en extremo de barra
        self.N1 = 0
        self.V1 = 0
        self.M1 = 0
        self.N2 = 0
        self.V2 = 0
        self.M2 = 0

        # Desplazamientos en extremo de barra
        self.dx1 = 0
        self.dy1 = 0
        self.gz1 = 0
        self.dx2 = 0
        self.dy2 = 0
        self.gz2 = 0

        # Tensión máxima que debe soportar la barra
        self.Tmax = 0
        self.p = 0 # Porcentaje de aprovechamiento del perfil

        # Matrices de la barra
        self.k = 0 # Matriz de rigidez
        self.r = 0 # Matriz de rotacion

    def set_material(self, E, d, fyd):
        """ Establece las propiedades del material de la barra """
        self.E = E
        self.d = d
        self.fyd = fyd

    def set_properties(self, A, Iz, Wz):
        """ Establece las propiedades de la barra """
        self.A = A
        self.P = self.L * (A / 1000000) * self.d
        self.Iz = Iz
        self.Wz = Wz

    def set_efforts(self, N1, V1, M1, N2, V2, M2):
        (self.N1, self.V1, self.M1, self.N2, self.V2, self.M2) = (N1, V1, M1, N2, V2, M2)

    def set_displacements(self, dx1, dy1, gz1, dx2, dy2, gz2):
        (self.dx1, self.dy1, self.gz1, self.dx2, self.dy2, self.gz2) = (dx1, dy1, gz1, dx2, dy2, gz2)

    # Momentos
    def M(self, x):
        """ Calcula el momento en un punto """
        M = - self.M1 + self.V1 * x + self.qy * x * x / 2
        return M

    # Deformada
    def y(self, x):
        """ Calcula la deformada en un punto """
        y = (-1. / (self.E * self.Iz)) * (self.M1 * x**2 / 2 - self.V1 * x**3 / 6 - self.qy * x**4 / 24) + self.gz1 * x + self.dy1
        return y

    def draw_member(self):
        """ Dibuja la barra """
        plot([self.X1, self.X2], [self.Y1, self.Y2], color='gray', lw=2)

    def draw_loads(self, scale):
        """ Dibuja las cargas sobre la barra """
        if self.qY != 0:
            YL1 = self.Y1 + scale * abs(self.qy)
            YL2 = self.Y2 + scale * abs(self.qy)
            fill([self.X1, self.X1, self.X2, self.X2], [self.Y1, YL1, YL2, self.Y2], hatch='|', facecolor='black')
            txt = "%d" %self.qY
            text((self.X1 + self.X2)/2, (self.Y1 + self.Y2 + YL1 + YL2)/4, txt, va='center', ha='center', color='red')
        elif self.qy != 0:
            s = self.sin
            c = self.cos
            XL1 = self.X1 - scale * abs(self.qy) * s
            XL2 = self.X2 - scale * abs(self.qy) * s
            YL1 = self.Y1 + scale * abs(self.qy) * c
            YL2 = self.Y2 + scale * abs(self.qy) * c
            fill([self.X1, XL1, XL2, self.X2], [self.Y1, YL1, YL2, self.Y2], hatch='|', facecolor='black')
            txt = "%d" %self.qy
            text((self.X1 + self.X2 + XL1 + XL2)/4, (self.Y1 + self.Y2 + YL1 + YL2)/4, txt, va='center', ha='center', color='red')

    def draw_diagram(self, x, E, scale, color):
        """ Dibuja el diagrama de esfuerzos (E) """

        # Dibuja el diagrama
        X = x * self.cos + self.X1
        Y = x * self.sin + self.Y1
        X = X - (scale * self.sin * E)
        Y = Y + (scale * self.cos * E)
        X = [self.X1] + list(X) + [self.X2]
        Y = [self.Y1] + list(Y) + [self.Y2]
        fill(X, Y, facecolor=color)

        # Escribe los valores
        E1 = abs(round(E[0], 1))
        E2 = abs(round(E[-1], 1))
        if E1 == E2:
            txt = "\n %.1f \n" %E1
            text((X[0] + X[1] + X[-1] + X[-2])/4, (Y[0] + Y[1] + Y[-1] + Y[-2])/4, txt, va='center', ha='center', fontsize=9, color='black')
        else:
            txt = "\n %.1f \n" %E1
            if E1 > 0:
                text(X[1], Y[1], txt, va='bottom', ha='left', fontsize=9, color='black')
            elif E1 < 0:
                text(X[1], Y[1], txt, va='top', ha='left', fontsize=9, color='black')
            txt = "\n %.1f \n" %E2
            if E2 > 0:
                text(X[-2], Y[-2], txt, va='bottom', ha='right', fontsize=9, color='black')
            elif E2 < 0:
                text(X[-2], Y[-2], txt, va='top', ha='right', fontsize=9, color='black')

    def draw_normal(self, scale):
        """ Dibuja el diagrama de esfuerzos normales """

        # Calculo de normales (N)
        x = arange(0, 1.1, 0.5)
        x = x * self.L
        N = - self.N1 - self.qx * x

        self.draw_diagram(x, N, scale, 'red')

    def draw_shear(self, scale):
        """ Dibuja el diagrama de esfuerzos cortantes """

        # Calculo de cortantes (V)
        x = arange(0, 1.1, 0.5)
        x = x * self.L
        V = - self.V1 - self.qy * x

        self.draw_diagram(x, V, scale, 'green')

    def draw_moment(self, scale):
        """ Dibuja el diagrama de momentos flectores """

        # Calculo de momentos (M)
        x = arange(0, 1.1, 0.1)
        x = x * self.L
        M = - self.M1 + (self.V1 * x) + (self.qy * x * x/2)

        self.draw_diagram(x, -M, scale, 'blue')

        if self.qy != 0:
            # Momento maximo (x = - V1/qy)
            xmax = - self.V1 / self.qy
            Mmax = - self.M1 - ((self.V1 * self.V1) / (2 * self.qy))
            txt = "\n x = %.3f\n Mmax = %.1f\n\n\n" %(xmax, Mmax)
            text((self.X1 + self.X2)/2, (self.Y1 + self.Y2)/2, txt, verticalalignment='center', horizontalalignment='center', fontsize=9, color='red')
            
    def draw_displacement(self, scale = 100):
        """ Dibuja el diagrama de desplazamientos o estructura deformada """
        
        # Calculo de la deformada (y)
        x = arange(0, 1.1, 0.1)
        x = x * self.L
        y = self.y(x)

        # Dibuja el diagrama
        X = x * self.cos + self.X1
        Y = x * self.sin + self.Y1
        X = X - (scale * self.sin * y)
        Y = Y + (scale * self.cos * y)
        plot(X, Y, '--', color='green', lw=2)
