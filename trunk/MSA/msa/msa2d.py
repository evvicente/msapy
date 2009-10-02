# -*- coding: UTF-8 -*-
# Método matricial para el análisis de estructuras planas.

from pylab import *

from joint2d import *
from member2d import *
from properties import *

import re # Expresiones regulares
def load(filename):
    """ Carga los datos de la estructura a partir del archivo """

    file = open(filename, "r")
    rows = file.readlines()
    file.close()

    properties = []
    joints = []
    members = []
    for row in rows:
        row = row.replace(',', '.')
        values = row.split(';')

        if re.search('^P\d+', values[0]):
            # Definicion de las propiedades de los materiales
            name = values[1]
            A = float(values[2])
            E = float(values[3])
            Iz = float(values[4])
            Wz = float(values[5])
            fyd = float(values[6])
            properties.append(Properties(name, A, E, Iz, Wz, fyd))

        elif re.search('^N\d+', values[0]):
            # Definicion de los nudos de la estructura
            X = float(values[1])
            Y = float(values[2])
            type = values[3]
            FX = float(values[4])
            FY = float(values[5])
            MZ = float(values[6])
            joints.append(Joint(X, Y, FX, FY, MZ, type))

        elif re.search('^B\d+', values[0]):
            # Definicion de las barras de la estructura
            i = int(values[1])
            j = int(values[2])
            X1 = joints[i].X
            Y1 = joints[i].Y
            X2 = joints[j].X
            Y2 = joints[j].Y
            qy = float(values[3])
            #qY = float(values[4])
            members.append(Member(i, j, X1, Y1, X2, Y2, qy))
            type = values[4]
            for prop in properties:
                if prop.name==type:
                    members[-1].set_properties(prop.A, prop.E, prop.Iz, prop.Wz, prop.fyd)
            # Para resolver estructuras reticulas establecemos Iz=0
            for member in members:
                if (joints[member.i].type == 'hj') or (joints[member.j].type == 'hj'):
                    member.Iz = 0

    return joints, members

def get_stiffness_matrix(E, A, I, L):
    """ Calcula la matriz de rigidez local de una barra (k) """

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

def get_rotation_matrix(X1, Y1, X2, Y2):
    """ Calcula la matriz de rotación de la barra (r) cuyas coordenadas
    de los nudos inicial y final son (X1, Y1) y (X2, Y2) respectivamente """

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
    """ Añade la matriz de rigidez global de una barra (K)  a la matriz de
    rigidez de la estructura (S), siendo (i) y (j) los nudos inicial y final
    de la barra, respectivamente """

    i *= 3
    j *= 3
    S[i:i+3,i:i+3] += K[0:3,0:3]
    S[i:i+3,j:j+3] += K[0:3,3:6]
    S[j:j+3,j:j+3] += K[3:6,3:6]
    S[j:j+3,i:i+3] += K[3:6,0:3]
    
def add_load_vector(L, P, n):
    """ Añade un estado de carga a un nudo de la estructura """
    
    # P = Vector de cargas en un nudo
    n *= 3
    L[n:n+3,0] += P[0:3,0]

def get_structure_stiffness_matrix(joints, members):
    """ Calcula la matriz de rigidez de la estructura (S) """

    n = len(joints) # Numero de nudos
    S = matrix(zeros((n*3,n*3)))

    for member in members:
        print
        print "Calculo de la matriz de rigidez local (k) de la barra %d/%d" %(member.i, member.j)
        member.k = get_stiffness_matrix(member.E, member.A, member.Iz, member.L)
        print member.k
        print
        print "Calculo de la matriz de rotacion (r) de la barra %d/%d" %(member.i, member.j)
        member.r = get_rotation_matrix(member.X1, member.Y1, member.X2, member.Y2)
        print member.r
        print
        print "Calculo de la matriz de rigidez global (K) de la barra %d/%d" %(member.i, member.j)
        K = member.r.T * member.k * member.r
        print K

        add_stiffness_matrix(S, K, member.i, member.j)

    return S

def get_structure_load_vector(joints, members):
    """ Calcula el vector de cargas de la estructura (L) """

    n = len(joints) # Numero de nudos
    L = matrix(zeros((n*3))).T

    for member in members:
        p = matrix(member.get_loads()).T

        P = - member.r.T * p

        add_load_vector(L, P[0:3,0], member.i)
        add_load_vector(L, P[3:6,0], member.j)

    # Cargas aplicadas directamente en los nudos
    for n in range(len(joints)):
        add_load_vector(L, matrix(joints[n].get_loads()).T, n)

    return L

def set_restraints(joints, S, L):
    """ Impone las condiciones de contorno mediante la eliminación de
    los grados de libertad impedidos """

    # Definicion de los tipos de nudos
    # Restricciones de los nudos (dN): [dX, dY, rZ]
    #   dX = Desplazaminto horizontal impedido (0)
    #   dY = Desplazamiento vertical impedido (0)
    #   gZ = Giro impedido (0)
    types = {'fs':[0, 0, 0], # Empotramiento
             'hs':[0, 0, 1], # Apoyo articulado
             'rs':[1, 0, 1], # Apoyo articulado movil
             'rj':[1, 1, 1], # Nudo rigido
             'hj':[1, 1, 0]} # Nudo articulado

    dN = []
    for n in range(len(joints)):
        dN.append(types[joints[n].type])

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

def get_displacements(S, L):
    """ Calcula los desplazamientos de los nudos de la estructura """

    return solve(S, L)

def get_reactions(K, D, P):
    """ Calcula las reacciones en los apoyos de la estructura """

    return K * D - P

def get_efforts(members, D):
    """ Calcula los esfuerzos en los extremos de barra """

    d = matrix(zeros(6)).T
    f = matrix(zeros([6, len(members)]))
    for n in range(len(members)):
        i = members[n].i*3
        j = members[n].j*3

        d[0:3,0] = D[i:i+3,0]
        d[3:6,0] = D[j:j+3,0]

        d = members[n].r * d

        f[:,n] = members[n].k * d
        f[:,n] += matrix(members[n].get_loads()).T

    return f

def msa(joints, members):
    """ Método matricial para la resolución de estructuras planas """
    
    S = get_structure_stiffness_matrix(joints, members)
    print
    print "Calculo de la matriz de rigidez de la estructura (S)"
    print S

    K = matrix(S) # copia de la matriz de rigidez

    print
    print "Calculo del vector de cargas de la estructura (L)"
    L = get_structure_load_vector(joints, members)
    print L

    P = matrix(L) # copia del vector de cargas

    print
    print "Establecimiento de las condiciones de contorno"
    set_restraints(joints, S, L)

    print
    print "Calculo de los desplazamientos de los nudos (D)"
    D = get_displacements(S, L)
    print D
    
    print
    print "Calculo de las reacciones en los apoyos (R)"
    R = get_reactions(K, D, P)
    print R

    print
    print "Calculo de los esfuerzos en los extremos de las barras (f)"
    f = get_efforts(members, D)
    print f.T

    print
    print "Comprobacion del equilibrio global de la estructura"
    FX = 0
    FY = 0
    MZ = 0
    for n in range(len(joints)):
        k = n * 3
        FX += R[k] + P[k]
        FY += R[k+1] + P[k+1]
        MZ += R[k+2] + P[k+2]
    print "FX =", round(FX, 7)
    print "FY =", round(FY, 7)
    print "(no implementado) MZ =", round(MZ, 7)
    
    print
    print "Comprobacion del equilibrio local de cada barra"
    for n in range(len(members)):
        k = n * 3
        N1 = f[0,n]
        V1 = f[1,n]
        M1 = f[2,n]
        N2 = f[3,n]
        V2 = f[4,n]
        M2 = f[5,n]
        Fx = N1 + N2
        Fy = V1 + V2 + members[n].qy * members[n].L
        Mz = M1 + M2 + members[n].qy * members[n].L**2 / 2 + V2 * members[n].L
        print "Barra", n
        print "Fx = ", round(Fx, 7)
        print "Fy = ", round(Fy, 7)
        print "Mz = ", round(Mz, 7)
    
    # Asignacion de resultados
    
    # Asignacion de desplazamientos y reacciones a los nudos correspondientes
    for n in range(len(joints)):
        k = n*3
        joints[n].set_displacements(D[k,0], D[k+1,0], D[k+2,0])
        joints[n].set_reactions(R[k,0], R[k+1,0], R[k+2,0])

    # Asignacion de los esfuerzos en extremos a las barras correspondientes
    for n in range(len(members)):
        members[n].set_efforts(f[0,n], f[1,n], f[2,n], f[3,n], f[4,n], f[5,n])

    print
    print "Comprobacion resistente de las barras (implementacion parcial)"
    for member in members:
        print "Barra %d/%d" %(member.i, member.j)
        fy1 = abs(member.N1 / member.A + member.M1 / member.Wz)
        fy2 = abs(member.N2 / member.A + member.M2 / member.Wz)
        fy3 = abs(member.N1 / member.A + member.M(member.L / 2) / member.Wz)
        print "Esfuerzo normal en la seccion central de la barra:", round(fy3, 2)
        if fy1 > fy2:
            fy = fy1
        else:
            fy = fy2
        p = fy / member.fyd * 100
        if p > 100:
            print "Se ha sobrepasado la resistencia del perfil: %.2f%%" % round(p, 2)
        else:
            print "Porcentaje de aprovechamiento del perfil: %.2f%% [ OK ]" % round(p, 2)
            