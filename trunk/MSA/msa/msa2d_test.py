# -*- coding: latin-1 -*-
from numpy.testing import *

import msa2d
from pylab import *

class  Msa2dTestCase(TestCase):
    def setup(self):
        """Module-level setup"""
        print 'doing setup'

    def teardown(self):
        """Module-level teardown"""
        print 'doing teardown'

    def test_get_stiffness_matrix(self):
        """ Comprueba la generación de la matriz de rigidez de una barra """
        
        E = 1; A = 0.09; I = 0.000675; L = 4
        k = mat("[0.0225 0 0 -0.0225 0 0; 0 0.0001266 0.000253 0 -0.00013 0.000253; 0 0.0002531 0.000675 0 -0.00025 0.000338; -0.0225 0 0 0.0225 0 0; 0 -0.0001266 -0.000253 0 0.000127 -0.00025; 0 0.0002531 0.000338 0 -0.00025 0.000675]")
        
        result = msa2d.get_stiffness_matrix(E, A, I, L)
        assert_almost_equal(result, k, decimal=5)

    def test_get_rotation_matrix(self):
        """ Comprueba la generación de la matriz de rotación de una barra """
        pass

if __name__ == '__main__':
    run_module_suite()
