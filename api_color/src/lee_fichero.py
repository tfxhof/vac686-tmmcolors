import csv

import colorpy.illuminants
import colorpy.colormodels
import pandas as pd
from spyder_kernels.utils.lazymodules import pandas
from tmm import color
from numpy import pi, linspace, inf, array

def leer_fichero_si():

    df = pd.read_csv("/documets/m_Au.txt", delimeter= '\t')

    df = array(df)
    matriz = pd.DataFrame(df, columns=['A', 'B'])
    column_b = matriz['B']

    def leer_fichero_au():
        df = pd.read_csv("/documets/m_SI.txt", delimeter='\t')

        df = array(df)
        matriz = pd.DataFrame(df, columns=['A', 'B'])
        column_b = matriz['B']

