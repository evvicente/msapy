# -*- coding: latin-1 -*-

__author__="Jorge Rodríguez Araújo"
__date__ ="24-jun-2009"

from pylab import *

from joint import *
from member import *  

# Diagrama estructural
def draw_schematic(joints, members):
    """ Dibuja la estructura """

    title("Esquema estructural")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    # Dibuja los nudos
    for n in range(len(joints)):
        joints[n].draw_joint()
        joints[n].draw_loads()
    # Dibuja las barras
    for n in range(len(members)):
        members[n].draw_member()
        members[n].draw_loads(0.001)

# Diagrama de reacciones
def draw_reactions(joints, members):
    """ Dibuja las reacciones """
    
    title("Reacciones")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(joints)):
        joints[n].draw_joint()
        joints[n].draw_loads()
        joints[n].draw_reactions()
    for n in range(len(members)):
        members[n].draw_member()

# Diagrama de normales
def draw_normals(members):
    """ Dibuja el diagrama de esfuerzos normales """

    # Busca un factor de escala apropiado
    maxN = 0
    for n in range(len(members)):
        if members[n].N1 > maxN:
            maxN = members[n].N1
    scale = 1/maxN

    title("Diagrama de esfuerzos normales (N)   $\leftarrow \lfloor\\rceil \\rightarrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_normal(scale)

# Diagrama de cortantes
def draw_shears(members):
    """ Dibuja el diagrama de esfuerzos cortantes """

    title("Diagrama de esfuerzos cortantes (V)   $\downarrow \lfloor\\rceil \uparrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_shear(0.001)

# Diagrama de momentos
def draw_moments(members):
    """ Dibuja el diagrama de momentos """

    title("Diagrama de momentos flectores (M)   $\curvearrowright \lfloor\\rceil \curvearrowleft$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_moment(0.01)

def draw_displacements(joints, members):
    """ Dibuja los desplazamientos """

    title("Diagrama de desplazamientos (f)")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    grid(True)
    X = []
    Y = []
    scale = 100
    for n in range(len(joints)):
        X = X + [joints[n].X + scale * joints[n].dX]
        Y = Y + [joints[n].Y + scale * joints[n].dY]
        # Escribe los valores de los desplazamientos
        t = ":\n N%d:\n" %n
        t += "$u$ %f\n" %joints[n].dX
        t += "$v$ %f\n" %joints[n].dY
        t += "$\\theta$ %f\n" %joints[n].gZ
        text(X[-1], Y[-1], t, verticalalignment='top', horizontalalignment='center', fontsize=9, color='brown')
    plot(X, Y, '+') # Nudos desplazados
    for n in range(len(members)):
        i = members[n].i
        j = members[n].j
        plot([X[i], X[j]], [Y[i], Y[j]], '--', color='green', lw=2)

def draw_joint(joints, members):
    print "Mostrando la estructura..."

    # Schematic
    figure(1)
    draw_schematic(joints, members)
    
    figure(2)
    draw_normals(members)

    figure(3)
    draw_shears(members)

    figure(4)
    draw_moments(members)

    figure(5)
    draw_displacements(joints, members)

    show()

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
        
        # Definición de los nudos de la estructura
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
        
        # Definición de los miembros de la estructura
        if re.search('^B', l[0]):
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
def save(joints, members, filename="output.csv"):
    file = open(filename, "w")

    s = "Nudos;X;Y;u;v;r;N;V;M\n"
    for n in range(len(joints)):
        s += "N%d;%f;%f;%f;%f;%f;%f;%f;%f\n" %(n, joints[n].X, joints[n].Y, joints[n].dX, joints[n].dY, joints[n].gZ, joints[n].RX, joints[n].RY, joints[n].RMZ)
    s += "\n"
    s += "Barras;i;f;Ni;Vi;Mi;Nf;Vf;Mf\n"
    for n in range(len(members)):
        s += "B%d;N%d;N%d;%f;%f;%f;%f;%f;%f\n" %(n, members[n].i, members[n].j, members[n].N1, members[n].V1, members[n].M1, members[n].N2, members[n].V2, members[n].M2)
    s = s.replace('.',',')

    file.write(s)
    file.close()