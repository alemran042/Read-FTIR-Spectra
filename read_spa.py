import pathlib
import numpy as np
from numpy import log as ln
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.signal as sig
from scipy.optimize import curve_fit, fsolve, newton, minimize
import scipy.special as sps
import scipy.integrate as integrate
plt.rc('font', family='serif')
plt.rc('mathtext', fontset='cm')
np.seterr(divide='ignore', invalid='ignore')
from sympy import symbols, solve
#from LoadSpectrum import read_spa
from BaselineRemoval import BaselineRemoval
import cmath
import random
import math
import os
import pdb

## Prepared by Emran

def read_spa(filepath):
    '''
    Input
    Read a file (string) *.spa
    ----------
    Output
    Return spectra, wavelenght (nm), titles
    '''
    with open(filepath, 'rb') as f:
        f.seek(564)
        Spectrum_Pts = np.fromfile(f, np.int32, 1)[0]
        f.seek(30)
        SpectraTitles = np.fromfile(f, np.uint8,255)
        SpectraTitles = ''.join([chr(x) for x in SpectraTitles if x!=0])

        f.seek(576)
        Max_Wavenum=np.fromfile(f, np.single, 1)[0]
        Min_Wavenum=np.fromfile(f, np.single, 1)[0]
        # print(Min_Wavenum, Max_Wavenum, Spectrum_Pts)
        Wavenumbers = np.flip(np.linspace(Min_Wavenum, Max_Wavenum, Spectrum_Pts))

        f.seek(288);

        Flag=0
        while Flag != 3:
            Flag = np.fromfile(f, np.uint16, 1)

        DataPosition=np.fromfile(f,np.uint16, 1)
        f.seek(DataPosition[0])

        Spectra = np.fromfile(f, np.single, Spectrum_Pts)
    return Spectra, 1e7/Wavenumbers, SpectraTitles


data = read_spa('2018Apr16_N2_100_40K.SPA')
spectra, wavelength, title = data


#### Baseline correction ####
#############################
polynomial_degree=2 #only needed for Modpoly and IModPoly algorithm
baseObj=BaselineRemoval(spectra)

Modpoly_output=baseObj.ModPoly(polynomial_degree)
Imodpoly_output=baseObj.IModPoly(polynomial_degree)
Zhangfit_output=baseObj.ZhangFit()

### Plot raw data ###
#####################
plt.figure()
plt.plot(wavelength, Zhangfit_output)
plt.xlim(1000., 2400)
#plt.ylim(.5, 1.)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Reflectance')
#plt.show()



### Plot normalized data ###
############################

Modpoly_output = Modpoly_output/Modpoly_output.max()

#spectra = spectra/spectra.max()
wavelength = wavelength/1000.

plt.figure()
plt.plot(wavelength, Modpoly_output)
plt.xlim(1., 2.4)
#plt.ylim(.5, 1.)
plt.xlabel('Wavelength [µm]')
plt.ylabel('Reflectance')
plt.show()



"""
basepath = '.'
paths = [str(x) for x in list(pathlib.Path(basepath).rglob('*.spa'))]
#print('Files detected: {}'.format(len(paths)))

for path in paths:
  spectra_tmp, wavelength_tmp, title_tmp = read_spa(path)


print()
"""