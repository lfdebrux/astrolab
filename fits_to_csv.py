#!/usr/bin/python

import get_jpl_position as jpl
import os, sys, subprocess, StringIO

from utils import delta_ra,delta_dec,ra2deg,dec2deg
from get_data_from_asc import run_sextractor,find_target_in_catalogue
from get_number_rms import get_number_rms

UCAC4 = '/remote/aa_64bin/auto_astrom/ucac4_find_astrom.py'

def get_obs_details(fits):
	"""
	Find the name of the target in a fits file and the time and date of when
	the observation was made using gethead from WCSTools.
	"""
	target = subprocess.check_output(['gethead','OBJ_NAME',fits]).strip()
	date_time = subprocess.check_output(['gethead','DATE-OBS',fits]).strip()
	
	return target,date_time

def get_jpl_ra_dec(target,date_time):
	"""
	Find the position according to JPL Horizons for a target at a set
	data and time, date_time, and return as RA and Dec in tuple form
	"""
	jpl.set_target(target)
	jpl.set_time(date_time)
	
	ra_jpl, dec_jpl = jpl.get_ephemeris()
	
	ra_jpl, dec_jpl = ra_jpl.split(), dec_jpl.split()
	
	return ra_jpl,dec_jpl

def run_ucac4_astrom(fits):
	"""
	Get the most accurate astrometry available
	"""
	with open(os.devnull,"w") as devnull:
		subprocess.call([UCAC4,fits],stdout=devnull,stderr=devnull)

	return 'a'+fits

def get_astrom_ra_dec_snr_fwhm(fits,ra,dec):
	"""
	Get the information on the target by running the sextractor
	and reading the resultant catalogue
	"""
	ra,dec = ra2deg(ra),dec2deg(dec)
	try:
		catalogue = run_sextractor(fits)
		ra_astrom,dec_astrom,snr,fwhm = find_target_in_catalogue(catalogue,ra,dec)
	except RuntimeError:
		print 'Target Not Found in ', fits
		raise RuntimeError('Target Not Found in' + fits)
	
	return ra_astrom,dec_astrom,snr,fwhm

def get_fwhm(fits,ra,dec):
	ra = ':'.join(ra)
	dec = ':'.join(dec)
	
	fwhm = subprocess.check_output(['/home/astrolab/matt_laurence/get_fwhm.sh',fits,ra,dec])
	
	return fwhm

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description="Analyse a series of fits files for unknown objects, " \
												 "and save the positions and properties of these objects to one .csv file"
									)
	parser.add_argument('fits_files',metavar='fits',nargs='+',help='a fits file to analyse')
	parser.add_argument('output_file',metavar='csv',help='a csv file to store the data. Must end in .csv')

	args = parser.parse_args()

	if not '.csv' in args.output_file:
		raise ValueError('Write file is not a csv!')

	output = open(args.output_file, "w")
	headers = "Object,Date,Time,Ast.RA,Ast.Dec,JPL RA,JPL Dec,RA Delta,Dec Delta,Astrom Number,Astrom RMS,SNR,FWHM"
	output.write(headers)
	output.write("\n")

	cwd = os.getcwd()

	jpl.new_session()

	for file in args.fits_files:	
		try:
			dir = os.path.dirname(file)
			
			if not dir is '':
				os.chdir(dir)
		
			fits = os.path.basename(file)

			# get data from fits file
			target,date_time = get_obs_details(fits)
			ra_jpl,dec_jpl = get_jpl_ra_dec(target,date_time)
			fits = run_ucac4_astrom(fits)
			ra_astrom,dec_astrom,snr,fwhm = get_astrom_ra_dec_snr_fwhm(fits,ra_jpl,dec_jpl)
			astrom_number,astrom_rms = get_number_rms('astrom.lis')
		except RuntimeError:
			pass # make the syntax checker happier
		else:
			# format for csv
			ra_delta = str(3600*delta_ra(ra_jpl,ra_astrom)) # get difference in arcseconds
			dec_delta = str(3600*delta_dec(dec_jpl,dec_astrom)) # get difference in arcseconds
			date, time = date_time.split('T')
			snr = str(snr)
			fwhm = str(fwhm)
			ra_astrom, dec_astrom, ra_jpl, dec_jpl = map(' '.join,(ra_astrom, dec_astrom, ra_jpl, dec_jpl))
		
			print target, date_time, '|',
			print ra_jpl, dec_jpl, '|',
			print ra_astrom, dec_astrom, '|',
			print astrom_number, '|',
			print astrom_rms, '|', 
			print snr, '|',
			print fwhm

			# append to csv
			row = ','.join((target,date,time,ra_astrom,dec_astrom,ra_jpl,dec_jpl,ra_delta,dec_delta,astrom_number,astrom_rms,snr,fwhm))
			output.write(row)
			output.write("\n")
		finally:
			# always cleanup and chdir
			rm = "rm -f *.cat *.ASC *.dat *_new *.lis asc* ucac4_stars"
			rm += " " + fits
			subprocess.call(rm, shell=True)
			os.chdir(cwd)
	
	output.close()
