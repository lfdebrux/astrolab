import os,subprocess,sys
from math import sqrt
from utils import cleanup

# from jrl_utils import deg2dms,deg2hms

def run_sextractor(fits):
	"""
	Run sextractor with our private configuration,
	saving the results in a catalogue file named after
	the input fits file
	"""
	sextractor = os.path.join(os.environ['STARLINK_DIR'],'bin/extractor/sex')
	config_file = './ascfit.sex'

	catalogue = os.path.splitext(fits)[0] + '.cat'

	subprocess.call([sextractor,'-c',config_file,fits,'-CATALOG_NAME',catalogue])

	return catalogue

def find_target_in_catalogue(catalogue,ra,dec):
	
	with open(catalogue) as f:
		for line in f:
			# skip comments
			if line[0] is '#': continue

			ra_cat,dec_cat = map(float,line.split()[1:3])

			if round(ra-ra_cat,2) == 0 and round(dec-dec_cat,2) == 0:
				peak,background,fwhm = map(float,line.split()[7:])
				# ra_cat = deg2hms(ra_cat)
				# dec_cat = deg2dms(dec_cat)
				fwhm = fwhm * 3600
				snr = get_snr(peak,background)
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

	fits = sys.argv[1]
	ra = ra2deg(map(float,sys.argv[2].split(':')))
	dec = dec2deg(map(float,sys.argv[3].split(':')))

	catalogue = run_sextractor(fits)

	print find_target_in_catalogue(catalogue,ra,dec)

	cleanup(os.getcwd())