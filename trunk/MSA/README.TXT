= MSA =

Copyright (C) 2009 Jorge Rodríguez Araújo <grrodri@gmail.com>

MSA es una implementación libre (GPL) del método de la rigidez para la resolución de estructuras planas.

== Descripción ==

Con este desarrollo se pretende lograr una aplicación funcional que permita la resolución de todo tipo de estructuras planas.

Para facilitar y agilizar el desarrollo se ha optado por la implementación en Python, dado que se trata de un lenguaje sencillo, que dispone de potentes herramientas de cálculo matricial, es multiplataforma y además es libre.

== Instalación ==

Dado que esta aplicación se encuentra desarrollada completamente en Python, puede ser ejecutada en cualquier plataforma para la que se encuentren disponibles los paquetes Numpy y matplotlib.

Para ejecutar MSA en Windows, simplemente:
 * Instala los paquetes: [http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi Python], [http://downloads.sourceforge.net/sourceforge/numpy/numpy-1.3.0-win32-superpack-python2.5.exe Numpy] y [http://downloads.sourceforge.net/sourceforge/matplotlib/matplotlib-0.98.5.3.win32-py2.5.exe matplotlib]
 * Una vez instalados los paquetes anteriores, dado que aún no se dispone de instalador, descarga y descomprime la [http://code.google.com/p/msapy/downloads/list última versión] disponible de la aplicación.
 * Haz doble clic sobre el archivo "MSA.py" que se encuentra en el directorio principal.

== Estudio de una viga continua ==

Aunque esta aplicación aún se encuentra en fases tempranas de desarrollo, se pueden resolver estructuras reticuladas con cargas en los nudos y estructuras de nudos rigidos que además presenten cargas uniformemente distribuidas. A continuación se muestra un ejemplo en el que se estudia una viga continua de tres vanos.

=== Definición de la estructura ===

Para definir la estructura se puede utilizar la plantilla "template.xls" desde EXCEL o CALC con tal de guardar los datos en un archivo ".csv", valores separados por punto y coma.

[http://lh5.ggpht.com/_OQVfrwwtV00/SsdnXdeYElI/AAAAAAAAAMs/PyjKRM2_P8o/gui.png]

Para definir el tipo de nudo o apoyo se utiliza sus siglas en inglés, siendo:
 * Tipo de nudo: nudo rígido (rj) o articulado (hj)
 * Tipo de apoyo: empotramiento (fs), articulado (hs) o rodillo (rs)

NOTA: Aún no se pueden resolver estructuras mixtas, con nudos articulados y rigidos.

=== Resultados ===

[http://lh4.ggpht.com/_OQVfrwwtV00/SsdnXikKvLI/AAAAAAAAAMw/cEZn_PfdfT4/s640/schematic.png]

[http://lh4.ggpht.com/_OQVfrwwtV00/SsdnX4xRj_I/AAAAAAAAAM0/ZwUJExCpHnQ/s640/loads.png]

[http://lh4.ggpht.com/_OQVfrwwtV00/SsdnX7XV_oI/AAAAAAAAAM4/n8BeFvWsCcg/s640/reactions.png]

[http://lh3.ggpht.com/_OQVfrwwtV00/SsdogaGWDxI/AAAAAAAAAM8/39X1HViXv5g/s640/normals.png]

[http://lh5.ggpht.com/_OQVfrwwtV00/SsdogsCza1I/AAAAAAAAANA/aZzsXAkZrzg/s640/shears.png]

[http://lh6.ggpht.com/_OQVfrwwtV00/Ssdogvk0_BI/AAAAAAAAANE/z74hHh3RT4I/s640/moments.png]

== Planifación y Versiones ==

|| ~~ Versión 0.1: Implementación del método de la rigidez ~~ ||

 * v 0.1.0 (2009-06-15): Implementación del método matricial.
 * v 0.1.1 (2009-06-21): Corrección de errores.

|| ~~ Versión 0.2: Generación del esquema estructural ~~ ||

 * v 0.2.0 (2009-06-23): Generación del esquema estructural.
 * v 0.2.1 (2009-06-24): Corrección de errores.

|| ~~ Versión 0.3: Generación de los diagramas de esfuerzos ~~ ||

 * v 0.3.0 (2009-06-30): Generación de los diagramas de esfuerzos.
 * v 0.3.1 (2009-07-06): Corrección de errores.
 * v 0.3.5 (2009-07-16): Interfaz gráfica de usuario.
 * v 0.3.6 (2009-08-11): Corrección de errores.
 * v 0.3.7 (2009-09-17): Generación del informe de resultados.
 * v 0.3.8 (2009-10-03): Corrección de errores.
 * v 0.3.9 (2009-10-20): Comprobación del equilibrio estructural.

|| Versión 0.4: Comprobación resistente ||
|| Versión 0.5: Refactorización ||
|| Versión 0.6: Generación de hipótesis de carga ||
|| Versión 0.7: Comprobación a pandeo ||
