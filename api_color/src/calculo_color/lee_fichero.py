import pandas as pd
from scipy.interpolate import interp1d


def calcula_ruta(material):
    return f"../../documents/m_{material}.txt"


def leer_fichero(material):
    ruta = calcula_ruta(material)
    df = pd.read_csv(ruta, delimiter='\t')
    df['nk'] = df.apply(lambda fila: complex(fila.iloc[1], fila.iloc[2]), axis=1)
    df['lambda'] = df.iloc[:, 0]
    si_n_fn = interp1d(df['lambda'], df['nk'], kind='linear')
    # Si_n_data = si_n_fn(df['lambda'])

    return si_n_fn
