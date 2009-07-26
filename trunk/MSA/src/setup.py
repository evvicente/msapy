# -*- coding: latin-1 -*-
__author__="Jorge Rodríguez Araújo"
__date__ ="$24-jul-2009 12:15:46$"

from setuptools import setup,find_packages

setup (
  name = "MSA",
  version = '0.1',
  packages = find_packages(),
  
  #scripts = ["MSA.py"],

  # Declare your packages' dependencies here, for eg:
  install_requires=["numpy", "matplotlib"],

  author = "Jorge Rodríguez Araújo",
  author_email = "grrodri@gmail.com",

  summary = "MSA is a Python implementation of Matrix Stiffness Analysis",
  url = "http://code.google.com/p/msapy/",
  license = "GPL",
  long_description= "MSA is a solver of plane structures.",
)
