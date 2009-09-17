#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Método matricial para el análisis de estructuras planas.

__author__="Jorge Rodríguez Araújo"
__date__ ="17-jul-2009"

from pylab import *

from joint2d import *
from member2d import *

# Carga los datos de la estructura
import re # Expresiones regulares
def load(filename):
    """ Lee los datos de la estructura """

    file = open(filename, "r")
    str = file.readlines()
    file.close()

    joints = []
    for s in str:
        s = s.replace(',', '.')
        l = s.split(';')
        
        # Definici�n de los nudos de la estructura
        if re.search('^N', l[0]):
            X = float(l[1])
            Y = float(l[2])
            type = l[3]
            FX = float(l[4])
            FY = float(l[5])
            MZ = float(l[6])
            
            joints.append(Joint(X, Y, FX, FY, MZ, type))

    members = [] 
    for s in str:
        s = s.replace(',', '.')
        l = s.split(';')
        
        # Definici�n de los miembros de la estructura
        if re.search('^B', l[0]):
            i = int(l[1])
            j = int(l[2])
            X1 = joints[i].X
            Y1 = joints[i].Y
            X2 = joints[j].X
            Y2 = joints[j].Y
            qy = float(l[3])
            A = float(l[4])
            E = float(l[5])
            I = float(l[6])

            members.append(Member(i, j, X1, Y1, X2, Y2, E, A, I, qy))

    return joints, members

def get_stiffness_matrix(E, A, I, L):
    """ Calcula la matriz de rigidez local de una barra """

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

def get_rotation_matrix(joints, i, j):
    """ Calcula la matriz de rotaci�n de la barra que une los nudos i, j """

    X1 = joints[i].X
    Y1 = joints[i].Y
    X2 = joints[j].X
    Y2 = joints[j].Y

    L = sqrt( (X2-X1)**2 + (Y2-Y1)**2 )
    sin = (Y2-Y1) / L
    cos = (X2-X1) / L

    r = matrix(zeros((6,6)))
    r[0,0] = r[1,1] = r[3,3] = r[4,4] = cos
    r[0,1] = r[3,4] = sin
    r[1,0] = r[4,3] = -sin
    r[2,2] = r[5,5] = 1

    return r

def add_stiffness_matrix(S, K, i, j):
    """ A�ade la matriz de rigidez global de una barra (K) a la matriz de rigidez de la estructura (S) """

    # i = Nudo inicial de la barra
    # j = Nudo final de la barra
    i *= 3
    j *= 3
    S[i:i+3,i:i+3] += K[0:3,0:3]
    S[i:i+3,j:j+3] += K[0:3,3:6]
    S[j:j+3,j:j+3] += K[3:6,3:6]
    S[j:j+3,i:i+3] += K[3:6,0:3]
    
def add_load_vector(L, P, n):
    """ A�ade un estado de carga a un nudo de la estructura """
    
    # P = Vector de cargas en un nudo
    n *= 3
    L[n:n+3,0] += P[0:3,0]

# Definici�n de propiedades {'name':[E, A, Iz]}
#   E = M�dulo de elasticidad
#   A = Area de la secci�n de la barra
#   Iz = Momento de inercia de la secci�n
properties = {'IPN 200':[210000e6, 0, 21.4e-6], 'p2':[21000, 2, 100]}

def get_structure_stiffness_matrix(S, joints, members):
    """ Determina la matriz de rigidez de la estructura (S) """

    for n in range(len(members)):
        i = members[n].i
        j = members[n].j
        L = members[n].L
        E = members[n].E
        A = members[n].A
        I = members[n].I

        k = get_stiffness_matrix(E, A, I, L)
        r = get_rotation_matrix(joints, i, j)

        K = r.T * k * r

        add_stiffness_matrix(S, K, i, j)

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

def get_structure_load_vector(L, joints, members):
    """ Determina el vector de cargas de la estructura (L) """

    for n in range(len(members)):
        i = members[n].i
        j = members[n].j

        p = matrix(members[n].get_loads()).T
        r = get_rotation_matrix(joints, i, j)

        P = -r.T * p

        add_load_vector(L, P[0:3,0], i)
        add_load_vector(L, P[3:6,0], j)

    # Cargas aplicadas directamente en los nudos
    for n in range(len(joints)):
        add_load_vector(L, matrix(joints[n].get_loads()).T, n)

def msa(joints, members):
    """ M�todo matricial para la resoluci�n de estructuras planas """

    # Tipos de nudos
    # Restricciones de los nudos (dN): [dX, dY, rZ]
    #   dX = Desplazaminto horizontal impedido (0)
    #   dY = Desplazamiento vertical impedido (0)
    #   gZ = Giro impedido (0)
    types = {'fs':[0, 0, 0],
             'hs':[0, 0, 1],
             'rs':[1, 0, 1],
             'rj':[1, 1, 1],
             'hj':[1, 1, 0]}

    dN = []
    for n in range(len(joints)):
        dN.append(types[joints[n].type])

    # N�mero de nudos
    n = len(joints)

    # Se genera la matriz de rigidez de la estructura (S)
    S = matrix(zeros((n*3,n*3)))
    get_structure_stiffness_matrix(S, joints, members)
    K = matrix(S) # copia de la matriz de rigidez

    # Se genera el vector de cargas de la estructura (L)
    L = matrix(zeros((n*3))).T
    get_structure_load_vector(L, joints, members)
    P = matrix(L) # copia del vector de cargas

    # Se imponen las condiciones de contorno mediante la eliminaci�n de
    # los grados de libertad impedidos
    for n in range(len(joints)):
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

    # Se calculan los desplazamientos (D) y las reacciones (R)
    D = solve(S, L)
    R = K * D - P

    # Se imprimen los resultados
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

    # Se calculan los esfuerzos en los extremos de barra
    d = matrix(zeros(6)).T
    f = matrix(zeros([6, len(members)]))
    for n in range(len(members)):
        i = members[n].i*3
        j = members[n].j*3

        d[0:3,0] = D[i:i+3,0]
        d[3:6,0] = D[j:j+3,0]

        E = members[n].E
        A = members[n].A
        I = members[n].I
        L = members[n].L
        r = get_rotation_matrix(joints, members[n].i, members[n].j)

        d = r * d

        k = get_stiffness_matrix(E, A, I, L)

        f[:,n] = k * d
        f[:,n] += matrix(members[n].get_loads()).T

    print "Esfuerzos en los extremos de barra (f)"
    print f.T

    # Se asignan los desplazamientos y reacciones a los nudos correspondientes
    for n in range(len(joints)):
        k = n*3
        joints[n].set_displacements(float(D[k]), float(D[k+1]), float(D[k+2]))
        joints[n].set_reactions(float(R[k]), float(R[k+1]), float(R[k+2]))

    # Se asignan los esfuerzos en extremos a su correspondiente barra
    for n in range(len(members)):
        N1 = f[0,n]
        V1 = f[1,n]
        M1 = f[2,n]
        N2 = f[3,n]
        V2 = f[4,n]
        M2 = f[5,n]
        members[n].set_efforts(N1, V1, M1, N2, V2, M2)
