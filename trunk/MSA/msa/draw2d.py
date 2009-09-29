# -*- coding: UTF-8 -*-

from pylab import *

from joint2d import *
from member2d import *

# Escalas de dibujo
loads_scale = 0.001
normals_scale = 0.1
shears_scale = 0.1
moments_scale = 0.1

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
        txt = "\n %d" %n
        text(joints[n].X, joints[n].Y, txt, va='top', ha='left', fontsize=10, color='red')
    # Dibuja las barras
    for n in range(len(members)):
        members[n].draw_member()

# Diagrama de cargas
def draw_loads(joints, members):
    """ Dibuja la estructura cargada"""

    title("Hipotesis de carga")
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
        members[n].draw_loads(loads_scale)

# Diagrama de reacciones
def draw_reactions(joints, members):
    """ Dibuja las reacciones """

    title("Reacciones")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(joints)):
        joints[n].draw_loads()
        joints[n].draw_reactions()
    for n in range(len(members)):
        members[n].draw_member()
        members[n].draw_loads(loads_scale)

# Diagrama de normales
def draw_normals(members):
    """ Dibuja el diagrama de esfuerzos normales """

    title("Diagrama de esfuerzos normales (N)   $\leftarrow \lfloor\\rceil \\rightarrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_normal(normals_scale)

# Diagrama de cortantes
def draw_shears(members):
    """ Dibuja el diagrama de esfuerzos cortantes """

    title("Diagrama de esfuerzos cortantes (V)   $\downarrow \lfloor\\rceil \uparrow$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_shear(shears_scale)

# Diagrama de momentos
def draw_moments(members):
    """ Dibuja el diagrama de momentos """
   
    title("Diagrama de momentos flectores (M)   $\curvearrowright \lfloor\\rceil \curvearrowleft$")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    for n in range(len(members)):
        members[n].draw_moment(moments_scale)

# Diagrama de desplazamientos
def draw_displacements(joints, members, scale = 0.1):
    """ Dibuja los desplazamientos """
    title("Diagrama de desplazamientos (f)")
    xlabel("X")
    ylabel("Y")
    axis('equal')
    grid(True)
    X = []
    Y = []
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
        """x = arange(0, 1.1, 1)
        X0 = x * (joints[j].X - joints[i].X) + joints[i].X + scale * joints[i].dX
        Y0 = x * (joints[j].Y - joints[i].Y) + joints[i].Y + scale * joints[i].dY
        x = x * members[n].L
        y = scale * members[n].y(x, joints[i].gZ, joints[n].dX * members[n].sin + joints[n].dY * members[n].cos)
        X = X0 - y * members[n].sin
        Y = Y0 + y * members[n].cos
        plot(X, Y, '--', color='green', lw=2)"""

def get_draw_scales(members):
    """ Obtiene las escalas de dibujo de los diagramas """
    # Busca un factor de escala apropiado
    qmax = 0
    Nmax = 0
    Vmax = 0
    Mmax = 0
    lmin = 100
    for n in range(len(members)):
        if abs(members[n].qy) > qmax:
            qmax = abs(members[n].qy)
        if abs(members[n].N1) > Nmax:
            Nmax = abs(members[n].N1)
        if abs(members[n].V1) > Vmax:
            Vmax = abs(members[n].V1)
        if abs(members[n].M1) > Mmax:
            Mmax = abs(members[n].M1)
        if members[n].L < lmin:
            lmin = members[n].L

    sq = 0.1
    sN = 0.1
    sV = 0.1
    sM = 0.1
    if qmax != 0:
        sq = 0.1*lmin/qmax
    if Nmax != 0:
        sN = 0.1*lmin/Nmax
    if Vmax != 0:
        sV = 0.1*lmin/Vmax
    if Mmax != 0:
        sM = 0.1*lmin/Mmax
        
    return [sq, sN, sV, sM]

# Tipos de coacciones
JointType = {'fs':"empotramiento", 'hs':"apoyo articulado", 'rs':"rodillo",
             'rj':"nudo rigido", 'hj':"nudo articulado"}

# Genera el informe
def report(joints, members, filename="output/report.html"):
    """ Genera el informe resultado del analisis de la estructura """

    # Se escribe el informe

    file = open(filename, "w")

    s = """<HTML>
    <HEAD>
        <META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">
        <TITLE>Informe</TITLE>
        <LINK rel="stylesheet" type="text/css" href="style.css">
    </HEAD>
    <BODY><CENTER>
        <H1>Informe de resultados</H1>
        <H2>Problema</H2>
        <IMG src="schematic.png" alt="Esquema estructural"/>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=2>Coordenadas</TH><TH rowspan=2>Coacciones</TH></TR>
                <TR><TH>X [m]</TH><TH>Y [m]</TH></TR>
            </THEAD>
        <TBODY>"""
    for n in range(len(joints)):
        s += '<TR><td>%d</td><td>%.1f</td><td>%.1f</td><td>%s</td></TR>' %(n, joints[n].X, joints[n].Y, JointType[joints[n].type])
    s += """                    </TBODY>
                    </TABLE>
                    <BR>
                    <TABLE>
                        <THEAD>
                            <TR><TH rowspan=2>Barras</TH><TH></TH><TH colspan=4>Propiedades</TH></TR>
                            <TR><TH>L [m]</TH><TH>A [mm2]</TH><TH>E [N/mm2]</TH><TH>Iz [cm4]</TH><TH>Wz [cm3]</TH></TR>
                        </THEAD>
                        <TBODY>"""
    for n in range(len(members)):
        s += '<tr><td>%d/%d</td><td>%.1f</td><td>%d</td><td>%d</td><td>%.1f</td><td>%.1f</td></tr>' %(members[n].i, members[n].j, members[n].L, members[n].A, members[n].E, members[n].Iz, members[n].Wz)
    s += """            </TBODY>
        </TABLE><BR>
        <H2>Cargas</H2>
        <IMG src="loads.png" alt="Cargas"/>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Cargas</TH></TR>
                <TR><TH>FX [N]</TH><TH>FY [N]</TH><TH>MZ [Nm]</TH></TR>
            </THEAD>
        <TBODY>"""
    for n in range(len(joints)):
        s += '<TR><td>%d</td><td>%d</td><td>%d</td><td>%d</td></TR>' %(n, joints[n].FX, joints[n].FY, joints[n].MZ)
    s += """                    </TBODY>
                    </TABLE><BR>
                    <TABLE>
                        <THEAD>
                            <TR><TH rowspan=2>Barras</TH><TH colspan=2>Cargas</TH></TR>
                            <TR><TH>qx [N/m]</TH><TH>qy [N/m]</TH></TR>
                        </THEAD>
                        <TBODY>"""
    for n in range(len(members)):
        s += '<tr><td>%d/%d</td><td>%d</td><td>%d</td></tr>' %(members[n].i, members[n].j, members[n].qx, members[n].qy)
    s += """            </TBODY>
        </TABLE><BR>
        <H2>Reacciones</H2>
        <IMG src="reactions.png" alt="Reacciones"/>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Reacciones</TH></TR>
                <TR><TH>RX [N]</TH><TH>RY [N]</TH><TH>MZ [Nm]</TH></TR>
            </THEAD>
            <TBODY>"""
    for n in range(len(joints)):
        s += '<tr><td>%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(n, joints[n].RX, joints[n].RY, joints[n].RMZ)
    s += """            </TBODY>
        </TABLE><BR>
        <H2>Esfuerzos</H2>
        <IMG src="normals.png" alt="Normales"/>
        <IMG src="shears.png" alt="Cortantes"/>
        <IMG src="moments.png" alt="Momentos"/>
        <TABLE>
            <THEAD>
                <TR><TH>Barras</TH><TH>N1</TH><TH>V1</TH><TH>M1</TH><TH>N2</TH><TH>V2</TH><TH>M2</TH></TR>
            </THEAD>
            <TBODY>"""
    for n in range(len(members)):
        s += '<tr><td>%d/%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(members[n].i, members[n].j, members[n].N1, members[n].V1, members[n].M1, members[n].N2, members[n].V2, members[n].M2)
    s += """            </TBODY>
        </TABLE><BR>
        <H2>Desplazamientos</H2>
        <IMG src="displacements.png" alt="Desplazamientos"/>
        <TABLE>
            <THEAD>
                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Desplazamientos</TH></TR>
                <TR><TH>dX [m]</TH><TH>dY [m]</TH><TH>gZ [rad]</TH></TR>
            </THEAD>
            <TBODY>"""
    for n in range(len(joints)):
        s += '<tr><td>%d</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, joints[n].dX, joints[n].dY, joints[n].gZ)
    s += """                </TBODY>
            </TABLE>
        <P><BR>______________________________<BR>
	Informe generado mediante <A href="http://code.google.com/p/msapy">MSA</A>, con la aplicación del método matricial de la rigidez.<BR>
        <A href="http://code.google.com/p/msapy">MSA</A> - Copyright 2009, Jorge Rodríguez Araújo (grrodri@gmail.com).</P>
        </CENTER>
    </BODY>
</HTML>"""

    file.write(s)
    file.close()

    # Se calculan y asignan las escalas de dibujo
    global loads_scale, normals_scale, shears_scale, moments_scale
    [sq, sN, sV, sM] = get_draw_scales(members)
    loads_scale = sq
    normals_scale = sN
    shears_scale = sV
    moments_scale = sM
    
    # Se dibujan y guardan todos los diagramas
    fig = figure(1)
    # Schematic
    fig.clear()
    draw_schematic(joints, members)
    savefig('output/schematic.png')
    # Loads
    fig.clear()
    draw_loads(joints, members)
    savefig('output/loads.png')
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
