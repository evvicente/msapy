
__author__="Jorge"
__date__ ="$24-jun-2009 16:02:23$"

from pylab import *

def drawJoints(N, dN):
    """ Dibuja los nudos """
    for n in range(len(N)):
        # Respresenta los apoyos
        if dN[n] == [0,0,0]:
            t = "$\\bot$\n"
        elif dN[n] == [0,0,1]:
            t = "$\\bigtriangleup$\n"
        elif dN[n] == [1,0,1]:
            t = "$\\triangleq$\n"
        else:
            t = "\n"
        text(N[n][0], N[n][1], t, verticalalignment='top', horizontalalignment='center', fontsize=18, color='black')

def drawMembers(N, B):
    """ Dibuja las barras """
    for n in range(len(B)):
        i = B[n][0]
        j = B[n][1]
        X1 = N[i][0]
        X2 = N[j][0]
        Y1 = N[i][1]
        Y2 = N[j][1]
        plot([X1, X2], [Y1, Y2], color='gray', linewidth=1.4)

def drawLoads(N, lN, B, lB):
    """ Dibuja las cargas """
    # Cargas en los nudos
    for n in range(len(N)):
        t = ""
        if lN[n][0] > 0:
            t = "$\\rightarrow$"
        elif lN[n][0] < 0:
            t = "$\\leftarrow$"
        text(N[n][0], N[n][1], t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if lN[n][1] > 0:
            t = "$\uparrow$"
        elif lN[n][1] < 0:
            t = "$\downarrow$"
        text(N[n][0], N[n][1], t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if lN[n][2] > 0:
            t = "$\circlearrowleft$"
        elif lN[n][2] < 0:
            t = "$\circlearrowright$"
        text(N[n][0], N[n][1], t, verticalalignment='bottom', horizontalalignment='center', fontsize=18, color='black')
        if lN[n] != [0,0,0]:
            t = "L%d:\n" %n
            if lN[n][0] != 0:
                t += "$N$ %.2f\n" %lN[n][0]
            if lN[n][1] != 0:
                t += "$V$ %.2f\n" %lN[n][1]
            if lN[n][2] != 0:
                t += "$M$ %.2f\n" %lN[n][2]
            t += ":\n"
            text(N[n][0], N[n][1], t, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='red')
    # Cargas en las barras
    for n in range(len(B)):
        i = B[n][0]
        j = B[n][1]
        X1 = N[i][0]
        X2 = N[j][0]
        Y1 = N[i][1]
        Y2 = N[j][1]
        if lB[n] != [0,0,0,0,0,0]:
            if B[n][5] != 0:
                fill_between([X1, X2], [Y1, Y2], [Y1+0.1, Y2+0.1], facecolor='red')
            t = ":\n :\n L%d:\n" %n
            t += "%f   $N$   %f\n" %(lB[n][0], lB[n][3])
            t += "%f   $V$   %f\n" %(lB[n][1], lB[n][4])
            t += "%f   $M$   %f\n" %(lB[n][2], lB[n][5])
            text((X1+X2)/2, (Y1+Y2)/2, t, verticalalignment='top', horizontalalignment='center', fontsize=9, color='red')

def drawDisplacements(N, D):
    """ Dibuja los desplazamientos """
    for n in range(len(N)):
        # Escribe los valores de los desplazamientos
        k = n*3
        t = ":\n :\n N%d:\n" %n
        t += "$u$ %f\n" %D[k]
        t += "$v$ %f\n" %D[k+1]
        t += "$\\theta$ %f\n" %D[k+2]
        text(N[n][0], N[n][1], t, verticalalignment='top', horizontalalignment='center', fontsize=9, color='green')

def drawEfforts(N, B, f):
    """ Dibuja los esfuerzos en los extremos de las barras """
    for n in range(len(B)):
        i = B[n][0]
        j = B[n][1]
        X1 = N[i][0]
        X2 = N[j][0]
        Y1 = N[i][1]
        Y2 = N[j][1]
        # Escribe los valores de los esfuerzos en extremo de barra
        t = "B%d:\n" %n
        t += "%f   $\\rightarrow$   %f\n" %(f[0,n], f[3,n])
        t += "%f   $\uparrow$   %f\n" %(f[1,n], f[4,n])
        t += "%f   $\circlearrowleft$   %f\n" %(f[2,n], f[5,n])
        t += ":\n"
        text((X1+X2)/2, (Y1+Y2)/2, t, verticalalignment='bottom', horizontalalignment='center', fontsize=9, color='blue')

# Dibuja la estructura
def draw(N, B, lN, dN, D, lB, f):
    print "Mostrando la estructura..."

    # Plot
    figure(1)
    title("Esquema estructural")
    xlabel("X")
    ylabel("Y")
    axis('equal')

    drawJoints(N, dN)
    drawLoads(N, lN, B, lB)
    drawMembers(N, B)

    figure(2)
    grid (True)

    drawJoints(N, dN)
    drawMembers(N, B)
    drawDisplacements(N, D)
    drawEfforts(N, B, f)

    show()

# Carga los datos de la estructura
import re
def load():
    print "Leyendo los datos de la estructura..."

    file = open("input.csv", "r")
    str = file.readlines()
    file.close()

    N = []
    dN = []
    lN = []
    B = []
    lB = []
    for s in str:
        s = s.split(';')
        if re.search('^N', s[0]):
            N.append([float(s[1]), float(s[2])])
            dN.append([float(s[3]), float(s[4]), float(s[5])])
            lN.append([float(s[6]), float(s[7]), float(s[8])])
        elif re.search('^B', s[0]):
            B.append([int(s[1]), int(s[2])])
            lB.append([0, 0, 0, 0, 0, 0])

    # Plot
    figure(1)
    title("Esquema estructural")
    xlabel("X")
    ylabel("Y")
    axis('equal')

    drawJoints(N, dN)
    drawLoads(N, lN, B, lB)
    drawMembers(N, B)

    show()

    return N, B

# Guarda los datos de la estructura
def save(N, B, D, R, f):
    print "Guardando los datos de la estructura..."

    file = open("output.csv", "w")

    s = "Nudos;X;Y;u;v;r;N;V;M\n"
    for n in range(len(N)):
        k = n*3
        s += "N%d;%f;%f;%f;%f;%f;%f;%f;%f\n" %(n, N[n][0], N[n][1], D[k], D[k+1], D[k+2], R[k], R[k+1], R[k+2])
    s += "\n"
    s += "Barras;i;f;Ni;Vi;Mi;Nf;Vf;Mf\n"
    for n in range(len(B)):
        s += "B%d;N%d;N%d;%f;%f;%f;%f;%f;%f\n" %(n, B[n][0], B[n][1], f[0,n], f[1,n], f[2,n], f[3,n], f[4,n], f[5,n])
    s = s.replace('.',',')

    file.write(s)
    file.close()

if __name__ == "__main__":
    load()