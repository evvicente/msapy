# -*- coding: latin-1 -*-

from distutils.core import setup

setup (name = "MSA",
       version = "0.3.7",
       description = "Python implementation of direct Matrix Stiffness Analysis for static structural solve",
       author = "Jorge Rodríguez Araújo",
       author_email = "grrodri@gmail.com",
       url = "http://code.google.com/p/msapy/",
       license = "GPL",
       packages = ['msa'],
       requires = ['numpy', 'matplotlib'],
     )
