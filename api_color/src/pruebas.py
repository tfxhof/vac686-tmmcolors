import math
import unittest
import calculo_color
from src.lee_fichero import leer_fichero_si


class TestMyModule(unittest.TestCase):

    def test_sum(self):
        d_list = [math.inf, 100, 10, math.inf]
        m_si = leer_fichero_si()
        m_au = leer_fichero_au()
        n_fn_list = [1, m_si, m_au, 1]
        th_0 = 0
        self.assertEqual(calculo_color.calcula_rgb(n_fn_list, d_list, th_0),0.7479 ,0.9396, 0.6148)


if __name__ == "__main__":
    unittest.main()
