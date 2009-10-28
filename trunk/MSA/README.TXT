== Presentación ==

¡Bienvenido/a a la página principal de MSA!

MSA es una implementación libre (GPL) del método matricial de la rigidez, con la que se pretende lograr una aplicación funcional que permita la resolución de todo tipo de estructuras planas.

Para facilitar y agilizar el desarrollo se ha optado por la implementación en Python, dado que se trata de un lenguaje sencillo, que dispone de potentes herramientas de cálculo matricial, es multiplataforma y además es libre.

== Modo de uso ==

Esta aplicación se encuentra completamente desarrollada en Python, y se apoya en las librerías Numpy y matplotlib, que le dan soporte para cálculo matricial y representación gráfica, respectivamente. Debido a esto, puede ser ejecutada en cualquier plataforma para la que se encuentren disponibles los anteriores paquetes.

Para ejecutar MSA en Windows, simplemente:
 * Instala los paquetes: [http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi Python], [http://downloads.sourceforge.net/sourceforge/numpy/numpy-1.3.0-win32-superpack-python2.5.exe Numpy] y [http://downloads.sourceforge.net/sourceforge/matplotlib/matplotlib-0.98.5.3.win32-py2.5.exe matplotlib]
 * Una vez instalados los paquetes anteriores, dado que aún no se dispone de instalador, descarga y descomprime la [http://code.google.com/p/msapy/downloads/list última versión] disponible de la aplicación.
 * Haz doble clic sobre el archivo "MSA.py" que se encuentra en el directorio principal.

Una vez ejecutada la aplicación, te encontrarás con una interfaz minimalista tal que:

[http://lh5.ggpht.com/_OQVfrwwtV00/Suhf68GBLaI/AAAAAAAAAO8/obnp9L4XCdg/text_gui.png]

Esta ventana pretende ofrecer la mayor simplicidad, de modo que se utiliza una ventana de texto para definir el problema y unos pocos botones para ejecutar las diferentes acciones.

[http://lh3.ggpht.com/_OQVfrwwtV00/Suhf6yhPuPI/AAAAAAAAAPA/mWO06JX3ngk/schematic_gui.png]

=== Definición de la estructura ===

Para definir la estructura también se puede utilizar la plantilla "template.xls" desde EXCEL (Office) o CALC ([http://www.openoffice.org OpenOffice]), dado que el archivo de definición de la estructura es de tipo ".csv" (valores separados por comas), con lo que sólo tendrás que seleccionar dicho formato a la hora de guardar el archivo.

Para definir el tipo de nudo o apoyo se utiliza sus siglas en inglés, siendo:
 * Tipo de nudo: nudo rígido (rj) o articulado (hj)
 * Tipo de apoyo: empotramiento (fs), articulado (hs) o rodillo (rs)

NOTA: Aún no se pueden resolver estructuras mixtas, con nudos articulados y rigidos.

== Casos de uso ==

Aunque esta aplicación aún se encuentra en fases tempranas de desarrollo, se pueden resolver estructuras reticuladas con cargas en los nudos y estructuras de nudos rigidos que además presenten cargas uniformemente distribuidas.

 * [http://code.google.com/p/msapy/wiki/VigaContinua Viga continua]
 * [http://docs.google.com/Doc?docid=0AZW-DvKrumg8ZGc3ZnE2c2dfNDhkN3dwZjNmaw&hl=es Estructura de nudos articulados]

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

|| ~~ Versión 0.4: Comprobación resistente ||

 * v 0.4.0 (2009-10-28): Comprobación resistente.

|| Versión 0.5: Refactorización ||
|| Versión 0.6: Generación de hipótesis de carga ||
|| Versión 0.7: Comprobación a pandeo ||

----
Copyright (C) 2009 Jorge Rodríguez Araújo <grrodri@gmail.com>