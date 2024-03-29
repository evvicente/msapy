== Presentaci�n ==

�Bienvenido/a a la p�gina principal de MSA!

MSA es una implementaci�n libre (GPL) del m�todo matricial de la rigidez, con la que se pretende lograr una aplicaci�n funcional que permita la resoluci�n de todo tipo de estructuras planas.

Para facilitar y agilizar el desarrollo se ha optado por la implementaci�n en Python, dado que se trata de un lenguaje sencillo, que dispone de potentes herramientas de c�lculo matricial, es multiplataforma y adem�s es libre.

== Modo de uso ==

Esta aplicaci�n se encuentra completamente desarrollada en Python, y se apoya en las librer�as Numpy y matplotlib, que le dan soporte para c�lculo matricial y representaci�n gr�fica, respectivamente. Debido a esto, puede ser ejecutada en cualquier plataforma para la que se encuentren disponibles los anteriores paquetes.

Para ejecutar MSA en Windows, simplemente:
 * Instala los paquetes: [http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi Python], [http://downloads.sourceforge.net/sourceforge/numpy/numpy-1.3.0-win32-superpack-python2.5.exe Numpy] y [http://downloads.sourceforge.net/sourceforge/matplotlib/matplotlib-0.98.5.3.win32-py2.5.exe matplotlib]
 * Una vez instalados los paquetes anteriores, dado que a�n no se dispone de instalador, descarga y descomprime la [http://code.google.com/p/msapy/downloads/list �ltima versi�n] disponible de la aplicaci�n.
 * Haz doble clic sobre el archivo "MSA.py" que se encuentra en el directorio principal.

Una vez ejecutada la aplicaci�n, te encontrar�s con una interfaz minimalista tal que:

[http://lh5.ggpht.com/_OQVfrwwtV00/Suhf68GBLaI/AAAAAAAAAO8/obnp9L4XCdg/text_gui.png]

Esta ventana pretende ofrecer la mayor simplicidad, de modo que se utiliza una ventana de texto para definir el problema y unos pocos botones para ejecutar las diferentes acciones.

[http://lh3.ggpht.com/_OQVfrwwtV00/Suhf6yhPuPI/AAAAAAAAAPA/mWO06JX3ngk/schematic_gui.png]

=== Definici�n de la estructura ===

Para definir la estructura tambi�n se puede utilizar la plantilla "template.xls" desde EXCEL (Office) o CALC ([http://www.openoffice.org OpenOffice]), dado que el archivo de definici�n de la estructura es de tipo ".csv" (valores separados por comas), con lo que s�lo tendr�s que seleccionar dicho formato a la hora de guardar el archivo.

Para definir el tipo de nudo o apoyo se utiliza sus siglas en ingl�s, siendo:
 * Tipo de nudo: nudo r�gido (rj) o articulado (hj)
 * Tipo de apoyo: empotramiento (fs), articulado (hs) o rodillo (rs)

NOTA: A�n no se pueden resolver estructuras mixtas, con nudos articulados y rigidos.

== Casos de uso ==

Aunque esta aplicaci�n a�n se encuentra en fases tempranas de desarrollo, se pueden resolver estructuras reticuladas con cargas en los nudos y estructuras de nudos rigidos que adem�s presenten cargas uniformemente distribuidas.

 * [http://code.google.com/p/msapy/wiki/VigaContinua Viga continua]
 * [http://docs.google.com/Doc?docid=0AZW-DvKrumg8ZGc3ZnE2c2dfNDhkN3dwZjNmaw&hl=es Estructura de nudos articulados]

== Planifaci�n y Versiones ==

|| ~~ Versi�n 0.1: Implementaci�n del m�todo de la rigidez ~~ ||

 * v 0.1.0 (2009-06-15): Implementaci�n del m�todo matricial.
 * v 0.1.1 (2009-06-21): Correcci�n de errores.

|| ~~ Versi�n 0.2: Generaci�n del esquema estructural ~~ ||

 * v 0.2.0 (2009-06-23): Generaci�n del esquema estructural.
 * v 0.2.1 (2009-06-24): Correcci�n de errores.

|| ~~ Versi�n 0.3: Generaci�n de los diagramas de esfuerzos ~~ ||

 * v 0.3.0 (2009-06-30): Generaci�n de los diagramas de esfuerzos.
 * v 0.3.1 (2009-07-06): Correcci�n de errores.
 * v 0.3.5 (2009-07-16): Interfaz gr�fica de usuario.
 * v 0.3.6 (2009-08-11): Correcci�n de errores.
 * v 0.3.7 (2009-09-17): Generaci�n del informe de resultados.
 * v 0.3.8 (2009-10-03): Correcci�n de errores.
 * v 0.3.9 (2009-10-20): Comprobaci�n del equilibrio estructural.

|| ~~ Versi�n 0.4: Comprobaci�n resistente ||

 * v 0.4.0 (2009-10-28): Comprobaci�n resistente.

|| Versi�n 0.5: Refactorizaci�n ||
|| Versi�n 0.6: Generaci�n de hip�tesis de carga ||
|| Versi�n 0.7: Comprobaci�n a pandeo ||

----
Copyright (C) 2009 Jorge Rodr�guez Ara�jo <grrodri@gmail.com>