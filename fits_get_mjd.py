'''
Reads DATE-OBS keyword in a FITS header and
finds the corresponding MJD.

Based on code at (accessed 2023-Oct-29):
https://docs.astropy.org/en/stable/time/


Usage: python fits_get_mjd.py input.fits

Output: MJD corresponding to DATE-OBS

Log:
2023-10-29: First working version (DM)
'''

# Import required functions or libraries
import sys
from astropy.io import fits
from astropy.time import Time

# Read the header
ipfile = sys.argv[1]
hdul=fits.open(ipfile)
hdr = hdul[0].header

# Comput the MJD from the value of DATE-OBS keyword
t = Time(hdr['DATE-OBS'], format='isot', scale='utc')
mjd = t.mjd

print(ipfile, mjd)

