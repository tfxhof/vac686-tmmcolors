import unittest
from calculo_color import calcula_rgb
from src.lee_fichero import leer_fichero
from numpy import pi, linspace, inf


class TestMyModule(unittest.TestCase):

    def test_sum(self):
        m_si = leer_fichero("si")
        m_au = leer_fichero("au")
        air_n_fn = lambda wavelength: 1
        n_fn_list = [air_n_fn, m_au, m_si]
        th_0 = 0
        d_list = [inf, 300, inf]
        resultado_esperado = [1.01182986, 0.77874535, 0.34523162]
        print(25)
        #resultado_obtenido=(calcula_rgb(n_fn_list, d_list, th_0))
        #self.assertEqual(calcula_rgb(n_fn_list, d_list, th_0), [1.01182986, 0.77874535, 0.34523162])
        resultado_obtenido = calcula_rgb(n_fn_list, d_list, th_0)
        for esperado, obtenido in zip(resultado_esperado, resultado_obtenido):
            self.assertAlmostEqual(esperado, obtenido, places=5)


if __name__ == "__main__":
    unittest.main()
