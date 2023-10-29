#!/usr/bin/env python


'''
Given two biases and flats, computes the gain (electrons/ADU) and
read noise (electrons) from a npix x npix region around the center
of these images.

Based on formulas given in Howell, Handbook of CCD Astronomy, pg 73.

Usage: get_gain_readnoise.py <bias1> <bias2> <flat1> <flat2> <npix>

Assumes that the image data is in fits extension [0]
'''

import sys
import numpy as np
from astropy.io import fits


bias1 = sys.argv[1]
bias2 = sys.argv[2]
flat1 = sys.argv[3]
flat2 = sys.argv[4]
npix  = sys.argv[5]

ww = int(npix//2)

# Read the central npix x npix region of each image
with fits.open(bias1) as hdul:
    xc = int(hdul[0].header['NAXIS1']//2)
    yc = int(hdul[0].header['NAXIS2']//2)
    dt = hdul[0].data
    b1 = dt[xc-ww:xc+ww, yc-ww:yc+ww]

with fits.open(bias2) as hdul:
    dt = hdul[0].data
    b2 = dt[xc-ww:xc+ww, yc-ww:yc+ww]

with fits.open(flat1) as hdul:
    dt = hdul[0].data
    f1 = dt[xc-ww:xc+ww, yc-ww:yc+ww]

with fits.open(flat2) as hdul:
    dt = hdul[0].data
    f2 = dt[xc-ww:xc+ww, yc-ww:yc+ww]


# Compute the averages
b1Avg = np.average(b1)
b2Avg = np.average(b2)
f1Avg = np.average(f1)
f2Avg = np.average(f2)

# Compute the standard deviation of the difference images
std_b12 = np.std(b1 - b2)
std_f12 = np.std(f1 - f2)

s2_b12 = std_b12 * std_b12
s2_f12 = std_f12 * std_f12

# Compute the gain and read noise
gain = ( (f1Avg+f2Avg) - (b1Avg+b2Avg) ) / (s2_f12-s2_b12)
rn = gain * std_b12 / np.sqrt(2)

print('gain (e-/ADU)= ',gain)
print('read noise (e-)= ', rn)
