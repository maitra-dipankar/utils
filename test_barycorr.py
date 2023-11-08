#!/usr/bin/env
# Using Shubham Kanodia's barycorrpy codes to get
# BJDTBD given JDUTC
#
# https://github.com/shbhuk/barycorrpy
# Kanodia and Wright 2018 Res. Notes AAS 2 4
# https://iopscience.iop.org/article/10.3847/2515-5172/aaa4b7

from astropy.time import Time
from barycorrpy import utc_tdb

# Time of observation, in JDUTC
JDUTC = Time(2458000, format='jd', scale='utc')

# Observation direction
RA, DEC = 123.456781, -54.321098

# For an observatory at lat, lon, altitude
LAT, LON, ALT = -45.16347, -71.423489, 8848.05

BJDTDB = utc_tdb.JDUTC_to_BJDTDB(JDUTC, ra=RA, dec=DEC, \
        lat=LAT, longi=LON, alt=ALT)
print(BJDTDB)



# For geocenter
from astropy.coordinates import EarthLocation
gc  = EarthLocation(0,0,0, unit="m")     # geocenter!
LAT = gc.lat.value
LON = gc.lon.value
ALT = gc.height.value


BJDTDB = utc_tdb.JDUTC_to_BJDTDB(JDUTC, ra=RA, dec=DEC, \
        lat=LAT, longi=LON, alt=ALT)
print(BJDTDB)

