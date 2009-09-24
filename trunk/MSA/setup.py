# -*- coding: latin-1 -*-

from distutils.core import setup
import py2exe

import matplotlib

setup (name = "MSA",
       version = "0.3.7",
       description = "Python implementation of direct Matrix Stiffness Analysis for static structural solve",
       author = "Jorge Rodriguez Araujo",
       author_email = "grrodri@gmail.com",
       url = "http://code.google.com/p/msapy/",
       license = "GPL",
       console = ['msa/MSA.py'],
       packages = ['msa'],
       #install_requires = ['numpy', 'matplotlib'],
       options = {'py2exe': {'packages' : ['matplotlib', 'pytz'],}},
       data_files = matplotlib.get_py2exe_datafiles()
     )
