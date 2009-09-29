from distutils.core import setup

setup (name = "MSA",
       version = "0.3.7",
       description = "Python implementation of direct Matrix Stiffness Analysis for static structural solve",
       author = "Jorge Rodriguez Araujo",
       author_email = "grrodri@gmail.com",
       url = "http://code.google.com/p/msapy/",
       license = "GPL",
       scripts = ['MSA.py'],  
       packages = ['msa'],
       #install_requires = ['numpy', 'matplotlib'],
     )
