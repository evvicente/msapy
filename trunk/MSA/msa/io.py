# -*- coding: UTF-8 -*-
from joint2d import *
from member2d import *
from properties import *

import draw2d

import re # Expresiones regulares
def load(filename):
    """ Carga los datos de la estructura a partir del archivo """

    file = open(filename, "r")
    rows = file.readlines()
    file.close()

    # Propiedades del material
    E = 0 # Modulo de elasticidad [N/mm2]
    fyd = 0 # Resistencia ultima [N/mm2]
    # Propiedades geometricas
    properties = load_properties() # Carga las propiedades definidas en data/properties.csv
    # Nudos
    joints = []
    # Barras
    members = []

    for row in rows:
        row = row.replace(',', '.')
        values = row.split(';')

        if re.search('^M\d+', values[0]):
            # Definicion de las propiedades del material
            name = values[1]
            E = float(values[2])
            d = float(values[3])
            fyd = float(values[4])
        elif re.search('^P\d+', values[0]):
            # Definicion de las propiedades de la barra
            name = values[1]
            A = float(values[2])
            Iz = float(values[3])
            Wz = float(values[4])
            properties.append(Properties(name, A, Iz, Wz))
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
                if prop.name == type:
                    members[-1].set_material(E, d, fyd)
                    members[-1].type = type
                    members[-1].set_properties(prop.A, prop.Iz, prop.Wz)

    return joints, members, properties

# Tipos de coacciones
JointType = {'fs':"empotramiento", 'hs':"apoyo articulado", 'rs':"rodillo",
             'rj':"nudo rigido", 'hj':"nudo articulado"}

# Genera el informe
def report(joints, members, filename="output/report.html"):
    """ Genera el informe resultado del analisis de la estructura """

    # Se escribe el informe

    file = open(filename, "w")

    s = '<HTML>'
    s += '    <HEAD>'
    s += '        <META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">'
    s += '        <TITLE>Informe</TITLE>'
    s += '        <LINK rel="stylesheet" type="text/css" href="style.css">'
    s += '    </HEAD>'
    s += '    <BODY><CENTER>'
    s += '        <H1>Informe de resultados</H1>'
    s += '        <H2>Problema</H2>'
    s += '        <IMG src="schematic.png" alt="Esquema estructural"/>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Nudos</TH><TH colspan=2>Coordenadas</TH><TH rowspan=2>Coacciones</TH></TR>'
    s += '                <TR><TH>X [m]</TH><TH>Y [m]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for n in range(len(joints)):
        s += '<TR><td>%d</td><td>%.1f</td><td>%.1f</td><td>%s</td></TR>' %(n, joints[n].X, joints[n].Y, JointType[joints[n].type])
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                 <TR><TH rowspan=2>Barras</TH><TH rowspan=2>Tipo</TH><TH colspan=2></TH><TH colspan=4>Propiedades</TH></TR>'
    s += '                 <TR><TH>Longitud [m]</TH><TH>Peso [kg]</TH><TH>A [mm2]</TH><TH>Iz [cm4]</TH><TH>Wz [cm3]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for member in members:
        s += '<tr><td>%d/%d</td><td>%s</td><td>%.1f</td><td>%.1f</td><td>%d</td><td>%.1f</td><td>%.1f</td></tr>' %(member.i, member.j, member.type, member.L, member.P, member.A, member.Iz, member.Wz)
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <H2>Cargas</H2>'
    s += '        <IMG src="loads.png" alt="Cargas"/>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Cargas</TH></TR>'
    s += '                <TR><TH>FX [N]</TH><TH>FY [N]</TH><TH>MZ [Nm]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for n in range(len(joints)):
        s += '<TR><td>%d</td><td>%d</td><td>%d</td><td>%d</td></TR>' %(n, joints[n].FX, joints[n].FY, joints[n].MZ)
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Barras</TH><TH colspan=2>Cargas</TH></TR>'
    s += '                <TR><TH>qx [N/m]</TH><TH>qy [N/m]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for member in members:
        s += '<tr><td>%d/%d</td><td>%d</td><td>%d</td></tr>' %(member.i, member.j, member.qx, member.qy)
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <H2>Reacciones</H2>'
    s += '        <IMG src="reactions.png" alt="Reacciones"/>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Reacciones</TH></TR>'
    s += '                <TR><TH>RX [N]</TH><TH>RY [N]</TH><TH>MZ [Nm]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for n in range(len(joints)):
        s += '<tr><td>%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(n, joints[n].RX, joints[n].RY, joints[n].RMZ)
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <H2>Esfuerzos</H2>'
    s += '        <IMG src="normals.png" alt="Normales"/>'
    s += '        <IMG src="shears.png" alt="Cortantes"/>'
    s += '        <IMG src="moments.png" alt="Momentos"/>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH>Barras</TH><TH>N1</TH><TH>V1</TH><TH>M1</TH><TH>N2</TH><TH>V2</TH><TH>M2</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for member in members:
        s += '<tr><td>%d/%d</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' %(member.i, member.j, member.N1, member.V1, member.M1, member.N2, member.V2, member.M2)
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <H3>Comprobación resistente</H3>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Barras</TH><TH rowspan=2>Tipo</TH><TH colspan=3>Tensiones máximas</TH></TR>'
    s += '                <TR><TH>Tensión [N/mm2]</TH><TH>Aprovechamiento [%]</TH><TH>Posición [m]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for member in members:
        s += '<TR><TD>%d/%d</TD><TD>%s</TD><TD>%.1f</TD><TD>%.2f</TD><TD>%s</TD></TR>' %(member.i, member.j, member.type, member.Tmax, member.p, '-')
    s += '            </TBODY>'
    s += '        </TABLE><BR>'
    s += '        <H2>Desplazamientos</H2>'
    s += '        <IMG src="displacements.png" alt="Desplazamientos"/>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Nudos</TH><TH colspan=3>Desplazamientos</TH></TR>'
    s += '                <TR><TH>dX [m]</TH><TH>dY [m]</TH><TH>gZ [rad]</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for n in range(len(joints)):
        s += '<tr><td>%d</td><td>%f</td><td>%f</td><td>%f</td></tr>' %(n, joints[n].dX, joints[n].dY, joints[n].gZ)
    s += '                </TBODY>'
    s += '            </TABLE><BR>'
    s += '        <H3>Comprobación a deformación</H3>'
    s += '        <TABLE>'
    s += '            <THEAD>'
    s += '                <TR><TH rowspan=2>Barras</TH><TH colspan=2>Flecha máxima absoluta</TH><TH colspan=2>Flecha máxima relativa</TH></TR>'
    s += '                <TR><TH>Pos [m]</TH><TH>Flecha [m]</TH><TH>Pos [m]</TH><TH>Flecha</TH></TR>'
    s += '            </THEAD>'
    s += '            <TBODY>'
    for member in members:
        s += '<TR><TD>%d/%d</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>' %(member.i, member.j, '-', '-', '-', '-')
    s += '                </TBODY>'
    s += '            </TABLE>'
    s += '        <P><BR>______________________________<BR>'
    s += '	Informe generado mediante <A href="http://code.google.com/p/msapy">MSA</A>, con la aplicación del método matricial de la rigidez.<BR>'
    s += '        <A href="http://code.google.com/p/msapy">MSA</A> - Copyright 2009, Jorge Rodríguez Araújo (grrodri@gmail.com).</P>'
    s += '        </CENTER>'
    s += '    </BODY>'
    s += '</HTML>'

    file.write(s)
    file.close()

    # Se dibujan y guardan todos los diagramas
    draw2d.draw(joints, members)
