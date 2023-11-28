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
        n_fn_list = [air_n_fn, m_si, m_au,air_n_fn]
        th_0 = 0
        d_list = [inf, 100, 10, inf]
        resultado_esperado = [174, 222, 149]
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, places=5)


if __name__ == "__main__":
    unittest.main()
