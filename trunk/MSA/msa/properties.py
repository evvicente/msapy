import csv

def load_properties(filename='properties.csv'):
    """ Carga la lista de propiedades de los materiales estructurales """

    rows = csv.reader(open(filename), delimiter=';', quotechar='"')    
    properties = []
    for row in rows:
        values = row
        if values[0]!="":
            name = values[0] # Designacion del perfil
            E = float(values[1]) # Modulo de elasticidad [N/mm2]
            A = float(values[2]) # Area de la seccion [mm2]
            Iz = float(values[3]) # Momento de inercia de la seccion [cm4]
            Wz = float(values[4]) # Modulo resistente [cm3]
            properties.append([name, A, E, Iz, Wz])
    return properties

if __name__ == "__main__":
    properties = load_properties()
    print properties

"""
# Definicion de propiedades {'name':[E, A, Iz]}
properties = {'IPN 200':[210000e6, 0, 21.4e-6],
              'p2':[21000, 2, 100]}

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