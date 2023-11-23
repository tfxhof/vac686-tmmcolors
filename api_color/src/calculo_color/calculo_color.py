import colorpy.illuminants
import colorpy.colormodels
from tmm import color


def calcula_rgb(n_fn_list, d_list, th_0):
    reflectances = color.calc_reflectances(n_fn_list, d_list, th_0)
    illuminant = colorpy.illuminants.get_illuminant_D65()
    spectrum = color.calc_spectrum(reflectances, illuminant)
    color_dict = color.calc_color(spectrum)
    return color_dict['irgb']
