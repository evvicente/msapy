# -*- coding: UTF-8 -*-

import csv

class Properties():
    def __init__(self, name, A, E, Iz, Wz):
        """ Define un conjunto de propiedades para un determinado material """

        # Designacion del perfil
        self.name = name 

        # Propiedades geometricas
        self.A = A # Area de la seccion [mm2]
        self.Iz = Iz # Momento de inercia de la seccion [cm4]
        self.Wz = Wz # Modulo resistente [cm3]

        # Modulo de elasticidad [N/mm2]
        self.E = E

    def set_loads(self, FX, FY, MZ):
        """ Establece las cargas en el nudo según los ejes globales """
        (self.FX, self.FY, self.MZ) = (FX, FY, MZ)

def load_properties(filename='properties.csv'):
    """ Carga la lista de propiedades de los materiales estructurales """

    rows = csv.reader(open(filename), delimiter=';', quotechar='"')    
    properties = []
    for row in rows:
        values = row
        if values[0]!="":
            name = values[0] 
            E = float(values[1]) 
            A = float(values[2]) 
            Iz = float(values[3]) 
            Wz = float(values[4]) 
            properties.append(Properties(name, A, E, Iz, Wz))
    return properties

if __name__ == "__main__":
    properties = load_properties()
    for prop in properties:
        print prop.name, prop.A, prop.E, prop.Iz, prop.Wz 

"""
# Prueba sqlite3
import sqlite3

db = sqlite3.connect('properties.db')
cursor = db.cursor()
cursor.execute("create table stocks (nombre text, edad integer)")
cursor.execute("insert into stocks values ('Jorge', '29')")
db.commit()
cursor.execute("select * from stocks")
db.commit()
data = cursor.fetchall()
for nombre, edad in data:
    print nombre, edad
cursor.close()
db.close()
"""
