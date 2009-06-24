#!/usr/bin/env python
# -*- coding: latin-1 -*-

__author__ = "Jorge Rodríguez Araújo <grrodri@gmail.com>"
__copyright__ = "Copyright (c) 2009 Jorge Rodríguez Araújo"
__license__ = "GPL"
__version__ = "0.2.1"
__date__ = "$20-jun-2009 11:42:12$"

from pylab import *

# Método matricial para el análisis de estructuras planas.
def msa():
    # Definición de la estructura
    #----------------------------------------------------------

    # Nudos (N): [X, Y]
    #   X = Coordenada horizontal en el eje de referencia absoluto
    #   Y = Coordenada vertical en el eje de referencia absoluto
    N = [[0, 0],
         [2, 0],
         [4, 0],
         [6, 0]]

    # Definición de propiedades {'name':[E, A, Iz]}
    #   E = Módulo de elasticidad
    #   A = Area de la sección de la barra
    #   Iz = Momento de inercia de la sección
    properties = {'IPN 200':[210000e6, 0, 21.4e-6], 'p2':[21000, 2, 100]}

    # Barras (B): [i, j, E, A, Iz]
    #   i = Nudo inicial de la barra
    #   j = Nudo final de la barra
    #   E = Módulo de elasticidad
    #   A = Area de la sección de la barra
    #   I = Momento de inercia de la sección
    #   q = Carga uniformemente distribuida
    B = [[0, 1, 210000e6, 0, 21.4e-6, -1200],
         [1, 2, 210000e6, 0, 21.4e-6, 0],
         [2, 3, 210000e6, 0, 21.4e-6, 0]]

    # Restricciones de los nudos (dN): [dX, dY, rZ]
    #   dX = Desplazaminto horizontal impedido (0)
    #   dY = Desplazamiento vertical impedido (0)
    #   rZ = Rotación impedida (0)
    dN = [[1, 1, 1],
          [1, 0, 1],
          [1, 1, 1],
          [0, 0, 1]]

    # Definición de las cargas
    #----------------------------------------------------------

    # Cargas en los nudos (lN): [FX, FY, MZ]
    #   FX = Carga según el eje horizontal
    #   FY = Carga según el eje vertical
    #   MZ = Momento según el eje Z
    #
    lN = [[0, 0, 0],
          [0, 0, 0],
          [0, -2000, 0],
          [0, 0, 0]]

    # Cargas en los extremos de las barras (lB): [Fxi, Fyi, Mzi, Fxj, Fyj, Mzj]
    #   Fxi = Carga en el nudo i según el eje x de la barra
    #   Fyi = Carga en el nudo i según el eje y de la barra
    #   Mzi = Momento en el nudo i según el eje z de la barra
    #   Fxj = Carga en el nudo j según el eje x de la barra
    #   Fyj = Carga en el nudo j según el eje y de la barra
    #   Mzj = Momento en el nudo j según el eje z de la barra
    lB = [[0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]

    # Calcula el número de nudos
    n = len(N)

    # Longitud de la barra
    def Length(i, j):
        """ Calcula la longitud de la barra que une los nudos i, j. """

        X1 = float(N[i][0])
        X2 = float(N[j][0])
        Y1 = float(N[i][1])
        Y2 = float(N[j][1])

        L = sqrt((X2 - X1)**2 + (Y2 - Y1)**2)

        return L

    # Carga uniforme
    def Uniform(q, L):
        """ Calcula las reacciones de empotramiento perfecto para una carga
        uniformente repartida en toda la barra. """

        V = -q*L/2
        M = q*L**2/12

        return [0, V, -M, 0, V, M]

    # Matriz de rigidez local
    def StiffnessMatrix(E, A, I, L):
        """ Define la matriz de rigidez local de la barra. """
        
        E = float(E)
        A = float(A)
        I = float(I)
        L = float(L)

        k = matrix(zeros((6,6)))
        k[0,0] = k[3,3] = (E*A/L)
        k[0,3] = k[3,0] = (-E*A/L)
        k[1,1] = k[4,4] = (12*E*I/L**3)
        k[4,1] = k[1,4] = (-12*E*I/L**3)
        k[1,2] = k[1,5] = k[2,1] = k[5,1] = (6*E*I/L**2)
        k[4,2] = k[4,5] = k[2,4] = k[5,4] = (-6*E*I/L**2)
        k[2,2] = k[5,5] = (4*E*I/L)
        k[2,5] = k[5,2] = (2*E*I/L)

        return k

    # Matriz de rotación
    def RotationMatrix(i, j):
        """ Define la matriz de rotación de la barra que une los nudos i, j. """

        X1 = float(N[i][0])
        X2 = float(N[j][0])
        Y1 = float(N[i][1])
        Y2 = float(N[j][1])

        L = sqrt( (X2-X1)**2 + (Y2-Y1)**2 )
        sin = (Y2-Y1) / L
        cos = (X2-X1) / L

        r = matrix(zeros((6,6)))
        r[0,0] = r[1,1] = r[3,3] = r[4,4] = cos
        r[0,1] = r[3,4] = sin
        r[1,0] = r[4,3] = -sin
        r[2,2] = r[5,5] = 1

        return r

    # Añade una barra a la matriz de rigidez de la estructura
    def AddStiffnessMatrix(S, K, i, j):
        # K = Matriz de rigidez global de la barra
        # i = Nudo inicial de la barra
        # j = Nudo final de la barra
        i *= 3
        j *= 3
        S[i:i+3,i:i+3] += K[0:3,0:3]
        S[i:i+3,j:j+3] += K[0:3,3:6]
        S[j:j+3,j:j+3] += K[3:6,3:6]
        S[j:j+3,i:i+3] += K[3:6,0:3]

    # Determina la matriz de rigidez de la estructura (S)
    def StructureStiffnessMatrix(S):
        for n in range(len(B)):
            i = B[n][0]
            j = B[n][1]
            L = Length(i, j)

            k = StiffnessMatrix(B[n][2], B[n][3], B[n][4], L)
            r = RotationMatrix(i, j)

            K = r.T * k * r

            AddStiffnessMatrix(S, K, i, j)

            print "#-------------------------------------------------"
            print "#  Barra %d:     Longitud = %0.2f m" %(n, L)
            print "#-------------------------------------------------"
            print " Matriz de rigidez local: k = "
            print k
            print
            print " Matriz de rotacion: r = "
            print r
            print
            print " Matriz de rigidez global: K = "
            print K
            print
            print " Matriz de rigidez de la estructura: S ="
            print S
            print

    # Añade un estado de carga a un nudo de la estructura
    def AddLoadVector(L, P, n):
        # P = Vector de cargas en un nudo
        n *= 3
        L[n:n+3,0] += P[0:3,0]

    # Determina el vector de cargas de la estructura (L)
    def StructureLoadVector(L):
        array(lB)
        for n in range(len(lB)):
            i = B[n][0]
            j = B[n][1]

            # Carga uniforme
            q = B[n][5]
            l = Length(i, j)
            if q != 0:
                lB[n] = Uniform(q, l)

            p = matrix(lB[n]).T
            r = RotationMatrix(i, j)

            P = -r.T * p

            AddLoadVector(L, P[0:3,0], B[n][0])
            AddLoadVector(L, P[3:6,0], B[n][1])

        # Cargas aplicadas directamente en los nudos
        for n in range(len(lN)):
            AddLoadVector(L, matrix(lN[n]).T, n)

    # Genera la matriz de rigidez de la estructura (S)
    S = matrix(zeros((n*3,n*3)))
    StructureStiffnessMatrix( S )
    K = matrix(S)
    # Genera el vector de cargas de la estructura (L)
    L = matrix(zeros((n*3))).T
    StructureLoadVector( L )
    P = matrix(L)

    # Se imponen las condiciones de contorno mediante la eliminación de
    # los grados de libertad impedidos
    for n in range(len(dN)):
        k0 = n*3
        k1 = k0 + 1
        k2 = k1 + 1

        if dN[n][0]==0:
            S[k0,:] = S[:,k0] = L[k0,0] = 0
            S[k0,k0] = 1
        if dN[n][1]==0:
            S[k1,:] = S[:,k1] = L[k1,0] = 0
            S[k1,k1] = 1
        if dN[n][2]==0:
            S[k2,:] = S[:,k2] = L[k2,0] = 0
            S[k2,k2] = 1
    # Artefacto parche
    for k in range(len(S)):
        if S[k,k] == 0:
            S[k,k] = 1

    # Solución del sistema

    # Desplazamientos (D)
    D = solve(S, L)
    # Reacciones (R)
    R = K * D - P

    # Resultados
    print
    print 'Matriz de rigidez de la estructura (S)'
    print S
    print
    print 'Vector de cargas de la estructura (L)'
    print L
    print
    print "Desplazamientos de los nudos (D)"
    print D
    print
    print "Reacciones (R)"
    print R
    print

    # Esfuerzos en los extremos de barra
    d = matrix(zeros(6)).T
    f = matrix(zeros([6, len(B)]))
    for n in range(len(B)):
        i = B[n][0]*3
        j = B[n][1]*3

        d[0:3,0] = D[i:i+3,0]
        d[3:6,0] = D[j:j+3,0]

        L = Length(B[n][0], B[n][1])
        r = RotationMatrix(B[n][0], B[n][1])

        d = r * d

        k = StiffnessMatrix(B[n][2], B[n][3], B[n][4], L)

        f[:,n] = k * d
        f[:,n] += matrix(lB[n]).T

    print "Esfuerzos en los extremos de barra: f = "
    print f.T
    print

    import msa_io
    msa_io.save(N, B, D, R, f)
    msa_io.draw(N, B, lN, dN, D, lB, f)

if __name__ == "__main__":
    msa()