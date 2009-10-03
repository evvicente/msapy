# -*- coding: UTF-8 -*-

from pylab import *

from joint2d import *
from member2d import *

# Escalas de dibujo
loads_scale = 0.001
normals_scale = 0.1
shears_scale = 0.1
moments_scale = 0.1
displacements_scale = 0.1

XYmax = 0
XYmin = 0

def create_figure(title_figure):
    fig = figure(1)
    fig.clear()
    
    title(title_figure)
    xlabel("X")
    ylabel("Y")
    axis('equal')
    #axis([XYmin, XYmax, XYmin, XYmax])

def draw_schematic(joints, members):
    """ Dibuja el esquema estructural """

    create_figure("Esquema estructural")
    for n in range(len(joints)):
        joints[n].draw_joint()
        txt = "\n %d" %n
        text(joints[n].X, joints[n].Y, txt, va='top', ha='left', fontsize=10, color='red')
    for member in members:
        member.draw_member()

def draw_loads(joints, members):
    """ Dibuja la estructura con sus estados de cargada """

    create_figure("Hipotesis de carga")
    for joint in joints:
        joint.draw_joint()
        joint.draw_loads()
    for member in members:
        member.draw_member()
        member.draw_loads(loads_scale)

def draw_reactions(joints, members):
    """ Dibuja la estructura y sus reacciones """

    create_figure("Reacciones")
    for joint in joints:
        joint.draw_loads()
        joint.draw_reactions()
    for member in members:
        member.draw_member()
        member.draw_loads(loads_scale)

def draw_normals(members):
    """ Dibuja el diagrama de esfuerzos normales """

    create_figure("Diagrama de esfuerzos normales (N)   $\leftarrow \lfloor\\rceil \\rightarrow$")
    for member in members:
        member.draw_normal(normals_scale)

def draw_shears(members):
    """ Dibuja el diagrama de esfuerzos cortantes """

    create_figure("Diagrama de esfuerzos cortantes (V)   $\downarrow \lfloor\\rceil \uparrow$")
    for member in members:
        member.draw_shear(shears_scale)

def draw_moments(members):
    """ Dibuja el diagrama de momentos flectores """
   
    create_figure("Diagrama de momentos flectores (M)   $\curvearrowright \lfloor\\rceil \curvearrowleft$")
    for member in members:
        member.draw_moment(moments_scale)

def draw_displacements(joints, members):
    """ Dibuja el diagrama de desplazamientos o estructura deformada """

    create_figure("Diagrama de desplazamientos (f)")
    grid(True)
    scale = displacements_scale
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
        #annotate("nota", xy=(0, 1), xycoords='data', xytext=(-50, 30), textcoords='offset points', arrowprops=dict(arrowstyle="->"))
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

def get_draw_scales(joints, members):
    """ Obtiene las escalas de dibujo de los diagramas """
    # Busca un factor de escala apropiado
    q = []
    N = []
    V = []
    M = []
    L = []
    lmin = 100
    for member in members:
        q += [abs(member.qy)]
        N += [abs(member.N1)]
        V += [abs(member.V1)]
        M += [abs(member.M1)]
        L += [abs(member.L)]
    
    qmax = array(q).max()
    Nmax = array(N).max()
    Vmax = array(V).max()
    Mmax = array(M).max()
    lmin = array(L).min()

    D = []
    XY = []
    for joint in joints:
        D += [abs(joint.dX), abs(joint.dY)]
        XY += [joint.X, joint.Y]
    Dmax = array(D).max()
    min = array(XY).min()
    max = array(XY).max()
    global XYmax, XYmin
    XYmax = max + 0.2 * (max - min)
    XYmin = min - 0.2 * (max - min)

    global loads_scale, normals_scale, shears_scale, moments_scale, displacements_scale
    if qmax != 0:
        loads_scale = 0.1 * lmin / qmax
    if Nmax != 0:
        normals_scale = 0.1 * lmin / Nmax
    if Vmax != 0:
        shears_scale = 0.1 * lmin / Vmax
    if Mmax != 0:
        moments_scale = 0.1 * lmin / Mmax
    if Dmax !=0:
        displacements_scale = 0.1 * lmin / Dmax

def draw(joints, members):
    """ Dibuja y guarda todos los diagramas estructurales """
    
    # Schematic
    draw_schematic(joints, members)
    savefig('output/schematic.png')
    # Loads
    draw_loads(joints, members)
    savefig('output/loads.png')
    # Reactions
    draw_reactions(joints, members)
    savefig('output/reactions.png')
    # Normals
    draw_normals(members)
    savefig('output/normals.png')
    # Shears
    draw_shears(members)
    savefig('output/shears.png')
    # Moments
    draw_moments(members)
    savefig('output/moments.png')
    # Displacements
    draw_displacements(joints, members)
    savefig('output/displacements.png')

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
    get_draw_scales(joints, members)
        
    # Se dibujan y guardan todos los diagramas
    draw(joints, members)
