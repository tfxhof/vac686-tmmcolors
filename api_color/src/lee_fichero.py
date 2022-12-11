import csv

import colorpy.illuminants
import colorpy.colormodels
import pandas as pd
from spyder_kernels.utils.lazymodules import pandas
from tmm import color

def leer_fichero():

    df = pd.read_csv("prueba.txt", delimeter= '\t')

    resul= round(df,3)

