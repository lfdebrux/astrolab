#!/usr/bin/python

import os,subprocess,sys
from math import sqrt
from utils import deg2dmstuple,deg2hmstuple

def run_sextractor(fits):
	"""
	Run sextractor with our private configuration,
	saving the results in a catalogue file named after
	the input fits file
	"""
	sextractor = os.path.join(os.environ['STARLINK_DIR'],'bin/extractor/sex')
	config_file = '/home/astrolab/matt_laurence/ascfit.sex'
	#config_file = '/Users/laurence/Coding/astrotmp/ascfit.sex'

	catalogue = os.path.splitext(fits)[0] + '.cat'

	subprocess.call([sextractor,'-c',config_file,fits,'-CATALOG_NAME',catalogue])

	return catalogue

def find_target_in_catalogue(catalogue,ra,dec):
	"""
	Read catalogue and return ra and dec according to sextractor,
	peak SNR, and FWHM in arcseconds
	"""
	ra_lim = dec_lim = 0.002 # look within ~5 arcsec
	found = False
	with open(catalogue) as f:
		for line in f:
			# skip comments
			if line[0] is '#': continue

			ra_cat,dec_cat = map(float,line.split()[1:3])

			# find closest match
			if abs(ra-ra_cat) < ra_lim and abs(dec-dec_cat) < dec_lim:
				ra_lim,dec_lim = abs(ra-ra_cat),abs(dec-dec_cat)
				# print ra_lim,dec_lim
				peak,background,fwhm = map(float,line.split()[7:])
				ra_obj = deg2hmstuple(ra_cat)
				dec_obj = deg2dmstuple(dec_cat)
				fwhm = fwhm * 3600 # convert to arcseconds
				snr = get_snr(peak,background)
				found = True
	if not found:
		raise RuntimeError('No match for the asteroid found')
	return ra_obj,dec_obj,snr,fwhm

def get_snr(peak,bg):
	"""
	Find the signal to noise ratio.
	Currently this finds the peak SNR,
	assuming sky limited conditions
	"""
	return peak/sqrt(bg)

if __name__ == '__main__':
	from utils import ra2deg,dec2deg

	fits = sys.argv[1]
	ra = ra2deg(map(float,sys.argv[2].split(':')))
	dec = dec2deg(map(float,sys.argv[3].split(':')))

	catalogue = run_sextractor(fits)

	print find_target_in_catalogue(catalogue,ra,dec)

	os.remove(catalogue) # cleanup after ourselves
