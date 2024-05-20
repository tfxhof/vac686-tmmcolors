import unittest
from src.calculo_color.calculo_color import calcula_rgb
from src.calculo_color.lee_fichero import leer_fichero
from numpy import inf


class TestMyModule(unittest.TestCase):

    def test_sum(self):
        m_si = leer_fichero("si")
        m_au = leer_fichero("au")
        air_n_fn = lambda wavelength: 1
        n_fn_list = [air_n_fn, m_si, m_au]
        th_0 = 0
        d_list = [inf, 100, inf]
        resultado_esperado = [190, 240, 156]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, places=5)

    def test_sum2(self):
        m_si = leer_fichero("si")
        m_au = leer_fichero("au")
        air_n_fn = lambda wavelength: 1
        n_fn_list = [air_n_fn, m_si, m_au, air_n_fn]
        th_0 = 0
        d_list = [inf, 100, 10, inf]
        resultado_esperado = [174, 222, 149]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, places=5)

    def test_sum3(self):
        m_Ga2O3 = leer_fichero("Ga2O3")
        m_Ag = leer_fichero("Ag")
        air_n_fn = lambda wavelength: 1
        n_fn_list = [air_n_fn, m_Ga2O3, m_Ag]
        th_0 = 0
        d_list = [inf, 2000, inf]
        resultado_esperado = [244, 187, 98]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, delta=5)

    def test_sum4(self):
        m_Ga2O3 = leer_fichero("Ga2O3")
        m_Ag = leer_fichero("Ag")
        air_n_fn = lambda wavelength: 1
        n_fn_list = [air_n_fn, m_Ga2O3, m_Ag, m_Ga2O3, m_Ag]
        th_0 = 0
        d_list = [inf, 2000, 3, 2000, inf]
        resultado_esperado = [226, 148, 82]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, delta=5)

    def test_sum5(self):
        m_Cu = leer_fichero("Cu")
        cu_n_fn = lambda wavelength: 1.5

        n_fn_list = [cu_n_fn, m_Cu, cu_n_fn]
        th_0 = 0
        d_list = [inf, 30, inf]
        resultado_esperado = [221, 160, 155]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, delta=5)

    def test_sum6(self):
        m_GaN = leer_fichero("GaN")
        m_Ga2O3 = leer_fichero("Ga2O3")
        m_Ag = leer_fichero("Ag")
        const1 = lambda wavelength: 1.33
        const2 = lambda wavelength: 5.0
        n_fn_list = [const1, m_GaN, m_Ga2O3, m_Ag, m_Ga2O3, m_GaN, const2]
        th_0 = 0
        d_list = [inf, 50, 30, 2, 30, 50, inf]
        resultado_esperado = [174, 112, 106]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, delta=5)

    def test_sum7(self):
        m_GaN = leer_fichero("GaN")
        m_Ga2O3 = leer_fichero("Ga2O3")
        const1 = lambda wavelength: 1
        const2 = lambda wavelength: 2
        n_fn_list = [const1, m_GaN, m_Ga2O3, m_GaN, m_Ga2O3, m_GaN, const2]
        th_0 = 0
        d_list = [inf, 50, 30, 50, 30, 50, inf]
        resultado_esperado = [124, 90, 165]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, delta=5)


if __name__ == "__main__":
    unittest.main()
