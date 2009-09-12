# -*- coding: latin-1 -*-

__author__="Jorge Rodríguez Araújo"
__date__ ="24-jun-2009"

from pylab import *

from joint2d import *
from member2d import *

# Diagrama estructural
def draw_schematic(joints, members):
    """ Dibuja la estructura """

    scale = 0.001
    # Busca un factor de escala apropiado
    max = 0
    for n in range(len(members)):
        if members[n].qy > max:
            max = members[n].qy
    if max != 0:
        scale = 0.1/max

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
        members[n].draw_loads(scale)

# Diagrama de reacciones
def draw_reactions(joints, members):
    """ Dibuja las reacciones """

    scale = 0.001
    # Busca un factor de escala apropiado
    max = 0
    for n in range(len(members)):
        if members[n].qy > max:
            max = members[n].qy
    if max != 0:
        scale = 0.1/max

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
        members[n].draw_loads(scale)

# Diagrama de normales
def draw_normals(members):
    """ Dibuja el diagrama de esfuerzos normales """

    scale = 0.01
    # Busca un factor de escala apropiado
    max = 0
    for n in range(len(members)):
        if members[n].N1 > max:
            max = members[n].N1
    if max != 0:
        scale = 0.1/max

    title("Diagrama de esfuerzos normales (N)   $\leftarrow \lfloor\\rceil \\rightarrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_normal(scale)

# Diagrama de cortantes
def draw_shears(members):
    """ Dibuja el diagrama de esfuerzos cortantes """

    scale = 0.001
    # Busca un factor de escala apropiado
    max = 0
    for n in range(len(members)):
        if members[n].V1 > max:
            max = members[n].V1
    if max != 0:
        scale = 0.1/max

    title("Diagrama de esfuerzos cortantes (V)   $\downarrow \lfloor\\rceil \uparrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_shear(scale)

# Diagrama de momentos
def draw_moments(members):
    """ Dibuja el diagrama de momentos """

    scale = 0.01
    # Busca un factor de escala apropiado
    max = 0
    for n in range(len(members)):
        if members[n].M1 > max:
            max = members[n].M1
    if max != 0:
        scale = 0.1/max
    
    title("Diagrama de momentos flectores (M)   $\curvearrowright \lfloor\\rceil \curvearrowleft$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_moment(scale)

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
    scale = 10
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

    s = """<HTML>
    <HEAD>
        <TITLE>Informe</TITLE>
        <STYLE type="text/css">
            H1 {text-align:center}
            H2 {text-align:center}
            IMG {width:600px; height:450px}
            TABLE {border-width:thin; border-style:solid; border-color:gray; font-size:11pt}
            THEAD {background-color:#DDDDDD}
            TD {text-align:center}
        </STYLE>
    </HEAD>
    <BODY><CENTER>
        <H1>Informe de resulados</H1>
        <H2>Problema</H2>
        <IMG src="schematic.png" alt="Esquema estructural"/>
        <P>El problema definido ha sido el siguiente:</P>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=2>Coordenadas</TH><TH colspan=3>Cargas</TH></TR>
                <TR><TH>X [m]</TH><TH>Y [m]</TH><TH>FX [N]</TH><TH>FY [N]</TH><TH>MZ [N·m]</TH></TR>
            </THEAD>
        <TBODY>"""
    for n in range(len(joints)):
        s += '<TR><td>%d</td><td>%.1f</td><td>%.1f</td><td>%d</td><td>%d</td><td>%d</td></TR>' %(n, joints[n].X, joints[n].Y, joints[n].FX, joints[n].FY, joints[n].MZ)
    s += """                    </TBODY>
                    </TABLE>
                    <BR>
                    <TABLE>
                        <THEAD>
                            <TR><TH rowspan=2>Barras</TH><TH></TH><TH colspan=3>Propiedades</TH><TH>Cargas</TH></TR>
                            <TR><TH>L [m]</TH><TH>A</TH><TH>E</TH><TH>Iz</TH><TH>qy [N/m]</TH></TR>
                        </THEAD>
                        <TBODY>"""
    for n in range(len(members)):
        s += '<tr><td>%d/%d</td><td>%.1f</td><td>%.5f</td><td>%.f</td><td>%.7f</td><td>%d</td></tr>' %(members[n].i, members[n].j, members[n].L, members[n].A, members[n].E, members[n].I, members[n].qy)
    s += """            </TBODY>
        </TABLE>
        <H2>Reacciones</H2>
        <IMG src="reactions.png" alt="Reacciones"/>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Reacciones</TH></TR>
                <TR><TH>RX [N]</TH><TH>RY [N]</TH><TH>MZ [N·m]</TH></TR>
            </THEAD>
            <TBODY>"""
    for n in range(len(joints)):
        s += '<tr><td>%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(n, joints[n].RX, joints[n].RY, joints[n].RMZ)
    s += """            </TBODY>
        </TABLE>
        <H2>Esfuerzos</H2>
        <IMG src="normals.png" alt="Normales"/>"""
    s += '<img src="shears.png" alt="Cortantes"/>'
    s += '<img src="moments.png" alt="Momentos"/>'
    s += '<table border="1">'
    s += '<thead>'
    s += '<tr><th>Barras</th><th>N1</th><th>V1</th><th>M1</th><th>N2</th><th>V2</th><th>M2</th></tr>'
    s += '</thead>'
    s += '<tbody>'
    for n in range(len(members)):
        s += '<tr><td>B%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(n, members[n].N1, members[n].V1, members[n].M1, members[n].N2, members[n].V2, members[n].M2)
    s += """            </TBODY>
        </TABLE>
        <H2>Desplazamientos</H2>
        <IMG src="displacements.png" alt="Desplazamientos"/>
        <TABLE border=1>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Desplazamientos</TH></TR>
                <TR><TH>dX [m]</TH><TH>dY [m]</TH><TH>gZ [rad]</TH></TR>
            </THEAD>
            <TBODY>"""
    for n in range(len(joints)):
        s += '<tr><td>N%d</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, joints[n].dX, joints[n].dY, joints[n].gZ)
    s += '</tbody>'
    s += '</table><br>'
    s += """        </CENTER></BODY>
</HTML>"""

    file.write(s)
    file.close()

    # Se dibujan y guardan todos los diagramas
    fig = figure(1)
    # Schematic
    fig.clear()
    draw_schematic(joints, members)
    savefig('output/schematic.png')
    # Reactions
    fig.clear()
    draw_reactions(joints, members)
    savefig('output/reactions.png')
    # Normals
    fig.clear()
    draw_normals(members)
    savefig('output/normals.png')
    # Shears
    fig.clear()
    draw_shears(members)
    savefig('output/shears.png')
    # Moments
    fig.clear()
    draw_moments(members)
    savefig('output/moments.png')
    # Displacements
    fig.clear()
    draw_displacements(joints, members)
    savefig('output/displacements.png')
