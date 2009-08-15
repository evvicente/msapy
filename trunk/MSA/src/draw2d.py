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

# Genera el informe
def report(joints, members, filename="output/report.html"):
    """ Genera el informe resultado del análisis de la estructura """

    # Se escribe el informe

    file = open(filename, "w")

    s = '<html><head><title></title></head><body><center>'
    s += '<img src="schematic.png" alt="Esquema estructural"/>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Nudos</th><th>X</th><th>Y</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(joints)):
        s += '<tr><td>N%d</td><td>%.2f</td><td>%.2f</td></tr>' %(n, joints[n].X, joints[n].Y)
    s += '</tbody>'
    s += '</table><br>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Barras</th><th>i</th><th>f</th><th>L</th><th>qy</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(members)):
        s += '<tr><td>B%d</td><td>N%d</td><td>N%d</td><td>%.f</td><td>%.1f</td></tr>' %(n, members[n].i, members[n].j, members[n].L, members[n].qy)
    s += '</tbody>'
    s += '</table><br>'
    s += '<img src="reactions.png" alt="Reacciones"/>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Nudos</th><th>RX</th><th>RY</th><th>RMZ</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(joints)):
        s += '<tr><td>N%d</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, joints[n].RX, joints[n].RY, joints[n].RMZ)
    s += '</tbody>'
    s += '</table><br>'
    s += '<img src="normals.png" alt="Normales"/>'
    s += '<img src="shears.png" alt="Cortantes"/>'
    s += '<img src="moments.png" alt="Momentos"/>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Barras</th><th>N1</th><th>V1</th><th>M1</th><th>N2</th><th>V2</th><th>M2</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(members)):
        s += '<tr><td>B%d</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, members[n].N1, members[n].V1, members[n].M1, members[n].N2, members[n].V2, members[n].M2)
    s += '</tbody>'
    s += '</table><br>'
    s += '<img src="displacements.png" alt="Desplazamientos"/>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Nudos</th><th>dX</th><th>dY</th><th>gZ</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(joints)):
        s += '<tr><td>N%d</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, joints[n].dX, joints[n].dY, joints[n].gZ)
    s += '</tbody>'
    s += '</table><br>'
    s += '</center></body></html>'

    file.write(s)
    file.close()

    # Se dibujan y guardan todos los diagramas

    # Schematic
    figure(1)
    draw_schematic(joints, members)
    savefig('output/schematic.png')
    # Reactions
    figure(2)
    draw_reactions(joints, members)
    savefig('output/reactions.png')
    # Normals
    figure(3)
    draw_normals(members)
    savefig('output/normals.png')
    # Shears
    figure(4)
    draw_shears(members)
    savefig('output/shears.png')
    # Moments
    figure(5)
    draw_moments(members)
    savefig('output/moments.png')
    # Displacements
    figure(6)
    draw_displacements(joints, members)
    savefig('output/displacements.png')
