#!/usr/bin/env python3

'''
Usage: type 

  python3 insert_wcs.py -h 

to see help on usage.

2022-Feb-19 (DM): Given a FITS image, do the following:
 (1) Get source positions using photutils, if photutils is installed, or
     send the entire image to DM's astrometry.net account (using DM's API key)
 (2) If astrometry.net is able to plate-solve the image, then get the
     WCS header information as python dictionary wcs_header.
 (3) Merge the original header with the wcs_header with a few edits (below):

     Remove the following headers from the top of wcs_header
      SIMPLE, BITPIX, NAXIS, EXTEND

     Add the following comments at the top of wcs_headers instead
       COMMENT Original key: "END"
       COMMENT
       COMMENT --Start of Astrometry.net WCS solution--
       COMMENT                                                                         
     And append the following comments at the end
       COMMENT
       COMMENT --End of Astrometry.net WCS--
       COMMENT

2023-Oct-29 (DM): Added command line options to pass input file name, 
       RA, DEC, search radius, plate scale upper and lower bound, and 
       parity. Giving an input file name is required. Giving RA, DEC, 
       search radius, plate scale bounds, and parity are optional. 
       See help for more details.
'''

import sys
import argparse

if len(sys.argv)==1:
    print('Type "insert_wcs.py -h" or "python3 insert_wcs.py -h" for help.')
    sys.exit(1)

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-i', type=str,
        help='Input file name', required=True)
parser.add_argument("-lo", type=float,
        help="Lower bound of image scale. Unit: arcseconds per pixel")
parser.add_argument("-hi", type=float,
        help="Upper bound of image scale. Unit: arcseconds per pixel")
parser.add_argument("-ra", type=float,
        help="RA of center for search. Unit: degrees [0.0 to 360.0]")
parser.add_argument("-dec", type=float,
        help="DEC of center for search. Unit: degrees [-90.0 to 90.0]")
parser.add_argument("-rad", type=float,
        help="Search radius. Unit: degrees")
parser.add_argument("-p", type=int, default=2, choices=[0, 1, 2],
        help="Image parity. Choices: 0, 1, 2. Default:2 => try both.")
args = parser.parse_args()


# ipfile='./calibrated_no_wcs.fits'     # For testing only
# center_ra=248.761598927,
# center_dec=38.2138723203, radius=0.9
# scale_type='ul', scale_lower=0.94, scale_upper=0.97,
# parity=1,

ipfile    = args.i
myra      = args.ra
mydec     = args.dec
myradius  = args.rad
myscaleLo = args.lo
myscaleHi = args.hi
myparity  = args.p

# Create the name of the output file
opfile = ipfile.replace(".fits", "_wcs.fits")


from astropy.io import fits
from astroquery.astrometry_net import AstrometryNet

# Read the original header
hdul=fits.open(ipfile)
hdr = hdul[0].header

# Now send the source positions to astrometry.net
ast = AstrometryNet()
ast.api_key = 'pbtyjiahmvhrucjn'

try_again = True
submission_id = None

while try_again:
    try:
        if not submission_id:
            if myscaleLo is not None:
                wcs_header = ast.solve_from_image(ipfile,
                        scale_units='arcsecperpix', scale_type='ul', 
                        scale_lower=myscaleLo, scale_upper=myscaleHi,
                        parity=myparity, center_ra=myra, center_dec=mydec,
                        radius=myradius, submission_id=submission_id)
            else:
                wcs_header = ast.solve_from_image(ipfile,
                        parity=myparity, center_ra=myra, center_dec=mydec,
                        radius=myradius, submission_id=submission_id)
        else:
            wcs_header = ast.monitor_submission(submission_id,
                                                solve_timeout=120)
    except TimeoutError as e:
        submission_id = e.args[1]
    else:
        # got a result, so terminate
        try_again = False


if wcs_header:
    # Code to execute when solve succeeds

    #Delete SIMPLE, BITPIX, NAXIS, EXTEND keywords from wcs_header
    del wcs_header['SIMPLE']
    del wcs_header['BITPIX']
    del wcs_header['NAXIS']
    del wcs_header['EXTEND']

    # Append stuff to write at the end of the combined header
    hdr.update(wcs_header)
    hdr.append(('COMMENT', ' '))
    hdr.append(('COMMENT', '--End of Astrometry.net WCS--'))
    hdr.append(('COMMENT', ' '))

    # Insert 4 lines of comment to indicate the beginning of the
    # WCS-related header
    nw=len(hdr) - len(wcs_header) + 4

    hdr.insert(nw+0, ('COMMENT', 'Original key: "END"'))
    hdr.insert(nw+1, ('COMMENT', ' '))
    hdr.insert(nw+2, ('COMMENT', '--Start of Astrometry.net WCS solution--'))
    hdr.insert(nw+3, ('COMMENT', ' '))

    # Write the new file with WCS header
    hdul.writeto(opfile,overwrite=True)
else:
    # Code to execute when solve fails
    print('Solve FAILED')


