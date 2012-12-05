import os,subprocess,sys
from math import sqrt

from jrl_utils import deg2dms,deg2hms

def find_target_in_catalogue(catalogue,ra,dec):
	file = open(catalogue)

	for line in file:
		# skip comments
		if line[0] is '#': continue

		ra_cat,dec_cat = map(float,line.split()[1:3])

		if round(ra-ra_cat,2) == 0 and round(dec-dec_cat,2) == 0:
			peak,background,fwhm = line.split()[7:]
			ra_cat = deg2hms(ra_cat)
			dec_cat = deg2dms(dec_cat)
			snr = get_snr(peak/bg)
			return ra_cat,dec_cat,snr,fwhm
	else:
		raise RuntimeError('No match for the asteroid found')

def get_snr(peak,bg):
	"""
	Find the signal to noise ratio.
	Currently this finds the peak SNR,
	assuming sky limited conditions
	"""
	return peak/sqrt(bg)

if __name__ == '__main__':
	from utils import ra2deg,dec2deg

	sextractor = os.path.join(os.environ['STARLINK_DIR'],'bin/extractor/sex')
	config_file = '/Users/laurence/Coding/astrolab/ascfit.sex'

	fits = sys.argv[1]
	ra = ra2deg(map(float,sys.argv[2].split(':')))
	dec = dec2deg(map(float,sys.argv[3].split(':')))

	subprocess.call([sextractor,'-c',config_file,fits])

	print find_target_in_catalogue('asc_sextr.cat')