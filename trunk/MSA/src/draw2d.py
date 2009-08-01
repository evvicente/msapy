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

    scale = 0.01
    # Busca un factor de escala apropiado
    maxN = 0
    for n in range(len(members)):
        if members[n].N1 > maxN:
            maxN = members[n].N1
    if maxN != 0:
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

# Diagrama de desplazamientos
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

# Dibuja todos los diagramas
def draw(joints, members):
    """ Dibuja todos los diagramas """

    figure(1)
    draw_schematic(joints, members)
    
    figure(2)
    draw_reactions(joints, members)
    
    figure(3)
    draw_normals(members)

    figure(4)
    draw_shears(members)

    figure(5)
    draw_moments(members)

    figure(6)
    draw_displacements(joints, members)

    show()
