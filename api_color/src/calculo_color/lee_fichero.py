import csv

import colorpy.illuminants
import colorpy.colormodels
import pandas as pd
from scipy.interpolate import interp1d
from spyder_kernels.utils.lazymodules import pandas
from tmm import color
from numpy import pi, linspace, inf, array as np


def calculaRuta(material):
    return f"../../documents/m_{material}.txt"


def leer_fichero(material):
    '''
    print(1)
    if material == "si":
        print(2)
        df = pd.read_csv("../../documents/m_Si.txt", delimiter='\t')
        print(3)
    elif material == "au":
        print(4)
        df = pd.read_csv("../../documents/m_Au.txt", delimiter='\t')
    else:
        raise ValueError("Material no compatible")
        print(5)
'''

    ruta = calculaRuta(material)
    df = pd.read_csv(ruta, delimiter='\t')
    print(ruta)
    print(df)
    df['nk'] = df.apply(lambda fila: complex(fila.iloc[1], fila.iloc[2]), axis=1)
    print(7)
    df['lambda'] = df.iloc[:,0]
    print(8)
    si_n_fn = interp1d(df['lambda'], df['nk'], kind='linear')
    #Si_n_data = si_n_fn(df['lambda'])

    return si_n_fn

    # coger columna labmda
