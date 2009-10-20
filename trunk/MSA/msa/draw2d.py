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

def create_figure(title_figure):
    fig = figure(1)
    fig.clear()
    
    title(title_figure)
    xlabel("X")
    ylabel("Y")
    axis('equal')

def show_schematic(joints, members):
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
    #for member in members:
    #    member.draw_displacement(displacements_scale)

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
    for joint in joints:
        D += [abs(joint.dX), abs(joint.dY), abs(joint.gZ)]
    Dmax = array(D).max()

    global loads_scale, normals_scale, shears_scale, moments_scale, displacements_scale
    if qmax != 0:
        loads_scale = 0.2 * lmin / qmax
    if Nmax != 0:
        normals_scale = 0.1 * lmin / Nmax
    if Vmax != 0:
        shears_scale = 0.3 * lmin / Vmax
    if Mmax != 0:
        moments_scale = 0.3 * lmin / Mmax
    if Dmax !=0:
        displacements_scale = 0.1 * lmin / Dmax

def get_draw_limits(joints):
    """ Obtiene los límites de dibujo """

    X = []
    Y = []
    for joint in joints:
        X += [joint.X]
        Y += [joint.Y]
    xmin = array(X).min()
    xmax = array(X).max()
    ymin = array(Y).min()
    ymax = array(Y).max()
    Xmax = xmax + 0.1 * (xmax - xmin)
    Xmin = xmin - 0.1 * (xmax - xmin)
    Ymax = ymax + 0.1 * (ymax - ymin)
    Ymin = ymin - 0.1 * (ymax - ymin)

    return [Xmin, Xmax, Ymin, Ymax]

def draw(joints, members):
    """ Dibuja y guarda todos los diagramas estructurales """

    # Se calculan y asignan las escalas de dibujo
    get_draw_scales(joints, members)
    # Limites de dibujo
    limits = get_draw_limits(joints)

    # Schematic
    show_schematic(joints, members)
    axis(limits)
    savefig('output/schematic.png')
    # Loads
    draw_loads(joints, members)
    axis(limits)
    savefig('output/loads.png')
    # Reactions
    draw_reactions(joints, members)
    axis(limits)
    savefig('output/reactions.png')
    # Normals
    draw_normals(members)
    axis(limits)
    savefig('output/normals.png')
    # Shears
    draw_shears(members)
    axis(limits)
    savefig('output/shears.png')
    # Moments
    draw_moments(members)
    axis(limits)
    savefig('output/moments.png')
    # Displacements
    draw_displacements(joints, members)
    axis(limits)
    savefig('output/displacements.png')
