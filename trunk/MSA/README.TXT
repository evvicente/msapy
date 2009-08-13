= MSA =

Copyright (C) 2009 Jorge Rodríguez Araújo <grrodri@gmail.com>

MSA es una implementación libre (GPL) del método de la rigidez para la resolución de estructuras planas.

== Descripción ==

Con este desarrollo se pretende lograr una aplicación funcional que permita la resolución de todo tipo de estructuras planas.

Para facilitar y agilizar el desarrollo se ha optado por la implementación en Python, dado que se trata de un lenguaje sencillo, que dispone de potentes herramientas de cálculo matricial, es multiplataforma y además es libre.

== Instalación ==

Dado que esta aplicación se encuentra desarrollada completamente en Python, puede ser ejecutada en cualquier plataforma para la que se encuentren disponibles los paquetes Numpy y matplotlib.

Para ejecutar MSA en Windows, simplemente:
 * Instala los paquetes: [Python http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi], [Numpy http://downloads.sourceforge.net/sourceforge/numpy/numpy-1.3.0-win32-superpack-python2.5.exe] y [matplotlib http://downloads.sourceforge.net/sourceforge/matplotlib/matplotlib-0.98.5.3.win32-py2.5.exe]
 * Una vez instalados los paquetes anteriores, dado que aún no se dispone de instalador, descarga y descomprime la última versión disponible de la aplicación.
 * Haz doble clic sobre el archivo "MSA.py" que se encunetra en el directorio "src/".

== Estudio de una viga de dos vanos ==

Aunque esta aplicación aún se encuentra en fases tempranas de desarrollo, a continuación, se muestra un ejemplo en el que se estudia una viga simple de dos vanos.

[http://lh5.ggpht.com/_OQVfrwwtV00/Sl-4mSvkeBI/AAAAAAAAALU/conExZ1ls-g/gui.png]

=== Definición de la estructura ===

Para definir la estructura se utiliza la plantilla "template.xls" desde EXCEL o CALC y se guardan los datos en el archivo "input.csv" como valores separados por punto y coma.

[http://lh6.ggpht.com/_OQVfrwwtV00/SlH49-N5U-I/AAAAAAAAAKo/aoBEHxIRF-s/beam.png]

En la columna "Restraints" se especifica el tipo de nudo (nudo rígido (rj) o articulado (hj)) o el tipo de apoyo (empotramiento (fs), articulado (hs) o rodillo (rs)).

=== Resultados ===

[http://lh4.ggpht.com/_OQVfrwwtV00/SlH497HvPMI/AAAAAAAAAKs/WgXoN1KS3v0/s640/beam-sch.png]

[http://lh5.ggpht.com/_OQVfrwwtV00/SlH4-IerEnI/AAAAAAAAAKw/v3Fy_6mLRZs/s640/beam-N.png]

[http://lh6.ggpht.com/_OQVfrwwtV00/SlH4-BPIakI/AAAAAAAAAK0/-0OrmM0YGLw/s640/beam-V.png]

[http://lh3.ggpht.com/_OQVfrwwtV00/SlH4-VOwPpI/AAAAAAAAAK4/xW6kWIMQnJg/s640/beam-M.png]

== Planifación ==

|| ~~ Versión 0.1: Implementación del método de la rigidez ~~ ||
|| ~~ Versión 0.2: Generación del esquema estructural ~~ ||
|| ~~ Versión 0.3: Generación de los diagramas de esfuerzos ~~ ||
|| Versión 0.4: Comprobación resistente ||
|| Versión 0.5: Refactorización ||
|| Versión 0.6: Generación de hipótesis de carga ||
|| Versión 0.7: Comprobación a pandeo ||

== Versiones ==

VERSION 0.3.6 2009-08-13
  * Corrección de errores. 

VERSION 0.3.5 2009-07-23
  * Interfaz gráfica de usuario.

VERSION 0.3.1 2009-06-11
  * Corrección de errores.

VERSION 0.3.0 2009-06-10
  * Generación de los diagramas de esfuerzos.

VERSION 0.2.1 2009-05-09
  * Corrección de errores.

VERSION 0.2.0 2009-05-03
  * Generación del esquema estructural.

VERSION 0.1.1 2009-04-27
  * Corrección de errores.

VERSION 0.1.0 2009-04-25
  * Implementación del método matricial.
