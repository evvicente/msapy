#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Jorge Rodríguez Araújo <grrodri@gmail.com>"
__copyright__ = "Copyright (c) 2009 Jorge Rodríguez Araújo"
__license__ = "GPL"
__version__ = "0.4.0"
__date__ = "28-oct-2009"

import os
import sys
import platform

from msa import gui, io, msa2d

if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.chdir(os.path.join(os.getcwd(), 'msa')) # Cambia el directorio de trabajo
        if platform.system() == "Windows":
            gui.run()
        if platform.system() == "Linux":
            gui.run()
    else:
        filename = sys.argv[1]  
        print "Leyendo los datos de definicion de la estructura..."
        (joints, members, properties) = io.load(filename)
        print "Resolviendo la estructura por el metodo de la rigidez..."
        msa2d.msa(joints, members, properties)
