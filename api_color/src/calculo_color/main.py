# -*- coding: utf-8 -*-
"""
Examples of plots and calculations using the tmm package.
"""
from matplotlib import pyplot as plt
from numpy import pi, linspace, inf
from src.calculo_color.calculo_color import calcula_rgb
from src.calculo_color.lee_fichero import leer_fichero

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from tmm import color

    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False

# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi / 180


def sample5():
    """
    Color calculations: What color is a air / thin SiO2 / Si wafer?
    """
    if not colors_were_imported:
        print('Colorpy was not detected (or perhaps an error occurred when',
              'loading it). You cannot do color calculations, sorry!',
              'Original version is at http://pypi.python.org/pypi/colorpy',
              'A Python 3 compatible edit is at https://github.com/fish2000/ColorPy/')
        return

    # Crystalline silicon refractive index. Data from Palik via
    # http://refractiveindex.info, I haven't checked it, but this is just for
    # demonstration purposes anyway.
    '''
    Si_n_data = [[400, 5.57 + 0.387j],
                   [450, 4.67 + 0.145j],
               [500, 4.30 + 7.28e-2j],
             [500, 4.30 + 7.28e-2j],
            [550, 4.08 + 4.06e-2j],
                   [650, 3.85 + 1.64e-2j],
           [700, 3.78 + 1.26e-2j]]
    
    
    Si_n_data = array(Si_n_data)
    Si_n_fn = interp1d(Si_n_data[:, 0], Si_n_data[:, 1], kind='linear')
    # SiO2 refractive index (approximate): 1.46 regardless of wavelength
    SiO2_n_fn = lambda wavelength: 1.46
    # air refractive index
    '''

    air_n_fn = lambda wavelength: 1
    au_n_fn = leer_fichero("au")
    si_n_fn = leer_fichero("si")

    n_fn_list = [air_n_fn, si_n_fn,au_n_fn, si_n_fn]
    th_0 = 0
    # Print the colors, and show plots, for the special case of 300nm-thick SiO2
    d_list = [inf, 100,200, inf]
    #muestra_graficas(n_fn_list, d_list, th_0)
    print('El rgb del sistema es:', calcula_rgb(n_fn_list, d_list, th_0))


def muestra_graficas(n_fn_list, d_list, th_0):
    reflectances = color.calc_reflectances(n_fn_list, d_list, th_0)
    illuminant = colorpy.illuminants.get_illuminant_D65()
    spectrum = color.calc_spectrum(reflectances, illuminant)
    color_dict = color.calc_color(spectrum)
    print('air / 300nm SiO2 / Si --- rgb =', color_dict['rgb'], ', xyY =', color_dict['xyY'])
    plt.figure()
    color.plot_reflectances(reflectances,
                            title='air / 300nm SiO2 / Si -- '
                                  'Fraction reflected at each wavelength')
    plt.figure()
    color.plot_spectrum(spectrum,
                        title='air / 300nm SiO2 / Si -- '
                              'Reflected spectrum under D65 illumination')

    # Calculate irgb color (i.e. gamma-corrected sRGB display color rounded to
    # integers 0-255) versus thickness of SiO2
    max_SiO2_thickness = 600
    SiO2_thickness_list = linspace(0, max_SiO2_thickness, num=80)
    irgb_list = []
    for SiO2_d in SiO2_thickness_list:
        d_list = [inf, SiO2_d, inf]
        reflectances = color.calc_reflectances(n_fn_list, d_list, th_0)
        illuminant = colorpy.illuminants.get_illuminant_D65()
        spectrum = color.calc_spectrum(reflectances, illuminant)
        color_dict = color.calc_color(spectrum)
        irgb_list.append(color_dict['irgb'])

    # Plot those colors
    print('Making color vs SiO2 thickness graph. Compare to (for example)')
    print('http://www.htelabs.com/appnotes/sio2_color_chart_thermal_silicon_dioxide.htm')
    plt.figure()
    plt.plot([0, max_SiO2_thickness], [1, 1])
    plt.xlim(0, max_SiO2_thickness)
    plt.ylim(0, 1)
    plt.xlabel('SiO2 thickness (nm)')
    plt.yticks([])
    plt.title('Air / SiO2 / Si color vs SiO2 thickness')
    for i in range(len(SiO2_thickness_list)):
        # One strip of each color, centered at x=SiO2_thickness_list[i]
        if i == 0:
            x0 = 0
        else:
            x0 = (SiO2_thickness_list[i] + SiO2_thickness_list[i - 1]) / 2
        if i == len(SiO2_thickness_list) - 1:
            x1 = max_SiO2_thickness
        else:
            x1 = (SiO2_thickness_list[i] + SiO2_thickness_list[i + 1]) / 2
        y0 = 0
        y1 = 1
        poly_x = [x0, x1, x1, x0]
        poly_y = [y0, y0, y1, y1]
        color_string = colorpy.colormodels.irgb_string_from_irgb(irgb_list[i])
        plt.fill(poly_x, poly_y, color_string, edgecolor=color_string)


if __name__ == "__main__":
    sample5()
