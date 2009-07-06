# -*- coding: latin-1 -*-
__author__="Jorge"
__date__ ="$24-jun-2009 16:02:23$"

from pylab import *

from joint import *
from member import *

def drawJoints(joints):
    """ Dibuja los nudos """
    
    for n in range(len(joints)):
        joints[n].draw()

def drawMembers(members):
    """ Dibuja las barras """

    for n in range(len(members)):
        members[n].draw()

def drawDisplacements(joints, D, members, scale):
    """ Dibuja los desplazamientos """
    X = []
    Y = []
    for n in range(len(joints)):
        k = n*3
        dX = float(D[k]) # Desplazamiento en X
        dY = float(D[k+1]) # Desplazamiento en Y
        X = X + [joints[n].X + scale * dX]
        Y = Y + [joints[n].Y + scale * dY]
        # Escribe los valores de los desplazamientos
        t = ":\n N%d:\n" %n
        t += "$u$ %f\n" %D[k]
        t += "$v$ %f\n" %D[k+1]
        t += "$\\theta$ %f\n" %D[k+2]
        text(X[-1], Y[-1], t, verticalalignment='top', horizontalalignment='center', fontsize=9, color='brown')
    plot(X, Y, '+') # Nudos desplazados
    for n in range(len(members)):
        i = members[n].i
        j = members[n].j
        plot([X[i], X[j]], [Y[i], Y[j]], '--', color='green', lw=2)

# Diagrama de normales
def drawNormals(members, f, scale):
    """ Dibuja el diagrama de esfuerzos normales """

    for n in range(len(members)):
        # Normales
        N1 = f[0,n]
        N2 = f[3,n]
        members[n].drawNormal(N1, N2, scale)

# Diagrama de cortantes
def drawShears(members, f, scale):
    """ Dibuja el diagrama de esfuerzos cortantes """

    for n in range(len(members)):
        # Cortantes
        V1 = f[1,n]
        V2 = f[4,n]
        members[n].drawShear(V1, V2, scale)

# Diagrama de momentos
def drawMoments(members, f, scale):
    """ Dibuja el diagrama de momentos """

    for n in range(len(members)):
        # Cortantes
        V1 = f[1,n]
        V2 = f[4,n]
        # Momentos
        M1 = f[2,n]
        M2 = f[5,n]
        members[n].drawMoment(V1, V2, M1, M2, scale)

# Dibuja la estructura
def draw(joints, members, D, f):
    print "Mostrando la estructura..."

    # Plot
    figure(1)
    title("Esquema estructural")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    drawJoints(joints)
    drawMembers(members)
    for n in range(len(joints)):
        joints[n].drawLoads()
    for n in range(len(members)):
        members[n].drawLoads(0.001)

    figure(2)
    title("Diagrama de esfuerzos normales (N)   $\leftarrow \lfloor\\rceil \\rightarrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    drawMembers(members)
    drawNormals(members, f, 0.01)

    figure(3)
    title("Diagrama de esfuerzos cortantes (V)   $\downarrow \lfloor\\rceil \uparrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    drawMembers(members)
    drawShears(members, f, 0.001)

    figure(4)
    title("Diagrama de momentos flectores (M)   $\curvearrowright \lfloor\\rceil \curvearrowleft$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    drawMembers(members)
    drawMoments(members, f, 0.01)

    figure(5)
    title("Diagrama de desplazamientos (f)")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    grid(True)
    drawMembers(members)
    drawDisplacements(joints, D, members, 100)

    show()

# Carga los datos de la estructura
import re # Expresiones regulares
def load(filename):
    print "Leyendo los datos de la estructura..."

    file = open(filename, "r")
    str = file.readlines()
    file.close()

    joints = []
    for s in str:
        s = s.replace(',', '.')
        l = s.split(';')
        
        # Definición de los nudos de la estructura
        if re.search('^N', l[0]):
            X = float(l[1])
            Y = float(l[2])
            type = l[3]
            FX = float(l[4])
            FY = float(l[5])
            MZ = float(l[6])
            
            joints.append(Joint(X, Y, FX, FY, MZ, type))

    n = 0
    members = [] 
    for s in str:
        s = s.replace(',', '.')
        l = s.split(';')
        
        # Definición de los miembros de la estructura
        if re.search('^B', l[0]):
            n += 1    
            i = int(l[1])
            j = int(l[2])
            X1 = joints[i].X
            Y1 = joints[i].Y
            X2 = joints[j].X
            Y2 = joints[j].Y
            qy = float(l[3])
            E = float(l[4])
            A = float(l[5])
            I = float(l[6])

            members.append(Member(i, j, X1, Y1, X2, Y2, E, A, I, qy))

    return joints, members

# Guarda los datos de la estructura
def save(joints, members, D, R, f):
    print "Guardando los datos de la estructura..."

    file = open("output.csv", "w")

    s = "Nudos;X;Y;u;v;r;N;V;M\n"
    for n in range(len(joints)):
        k = n*3
        s += "N%d;%f;%f;%f;%f;%f;%f;%f;%f\n" %(n, joints[n].X, joints[n].Y, D[k], D[k+1], D[k+2], R[k], R[k+1], R[k+2])
    s += "\n"
    s += "Barras;i;f;Ni;Vi;Mi;Nf;Vf;Mf\n"
    for n in range(len(members)):
        s += "B%d;N%d;N%d;%f;%f;%f;%f;%f;%f\n" %(n, members[n].i, members[n].j, f[0,n], f[1,n], f[2,n], f[3,n], f[4,n], f[5,n])
    s = s.replace('.',',')

    file.write(s)
    file.close()

if __name__ == "__main__":
    load()