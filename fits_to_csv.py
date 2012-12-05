#!/usr/bin/python

import find_jpl_position as jpl
import os, sys, subprocess, StringIO

from utils import *

output_filename = sys.argv[-1]

if not '.csv' in output_filename:
	raise ValueError('Write file is not a csv!')

output = open(output_filename, "w")
headers = "Object,Date,Time,Ast.RA,Ast.Dec,JPL RA,JPL Dec,RA Delta,Dec Delta,Astrom Number,Astrom RMS"
output.write(headers)
output.write("\n")

cwd = os.getcwd()

jpl.new_session()

for file in sys.argv[1:-1]:
	if not os.path.dirname(file) is '':
		os.chdir(os.path.dirname(file))
		
	fits = os.path.basename(file)
	
	target,date_time = get_obs_details(file)
	print target, date_time, '|',
	
	ra_jpl,dec_jpl = get_jpl_ra_dec(target,date_time)
	print ra_jpl, dec_jpl, '|',
	
	ra_astrom,dec_astrom = get_astrom_ra_dec(fits)
	
	ra_delta = str(delta_ra(ra_jpl,ra_astrom))
	dec_delta = str(delta_dec(dec_jpl,dec_astrom))
	
	fwhm = get_fwhm(file,ra_astrom,dec_astrom)
	
	ra_astrom, dec_astrom, ra_jpl, dec_jpl = map(' '.join,(ra_astrom, dec_astrom, ra_jpl, dec_jpl))
	
	print ra_astrom, dec_astrom, '|',
	print astrom_number, '|',
	print astrom_rms, '|', fwhm
	
	date, time = date_time.split('T')
	
	os.chdir(cwd)
	
	row = ','.join((target,date,time,ra_astrom,dec_astrom,ra_jpl,dec_jpl,ra_delta,dec_delta,astrom_number,astrom_rms))
	output.write(row)
	output.write("\n")

output.close()

def get_obs_details(fits):
	target = subprocess.check_output(['gethead','OBJ_NAME',fits]).strip()
	date_time = subprocess.check_output(['gethead','DATE-OBS',fits]).strip()
	
	return target,date_time

def get_jpl_ra_dec(target,date_time):
	jpl.set_target(target)
	jpl.set_time(date_time)
	
	ra_jpl, dec_jpl = jpl.get_ephemeris()
	
	ra_jpl, dec_jpl = ra_jpl.split(), dec_jpl.split()
	
	return ra_jpl,dec_jpl

def get_astrom_ra_dec(fits):
	astrom_command = '/remote/aa_64bin/auto_astrom/ucac4_find_astrom.py '
	astrom_command += fits
	astrom_command += ' | '
	astrom_command += "sed -n -e '/Got/p' -e '/Unknowns, 6/,/finished/p' -e '/RMS :/p'"
	
	astrom_new = StringIO.StringIO(subprocess.check_output(astrom_command, shell=True))
	
	cleanup(os.getcwd())
	
	i=0
	for line in astrom_new:
		if 'Got' in line:
			astrom_number = line.split()[1]
		if 'RMS :' in line:
			i+=1
			if i == 4:
				astrom_rms = line.split()[2]
		if '->' in line:
			ra_astrom = line.split()[3:6]
			dec_astrom = line.split()[6:10]
			
			#print ra_astrom, dec_astrom,
			
			if ra_astrom[0:2] == ra_jpl[0:2] and dec_astrom[0:2] == dec_jpl[0:2]:
				if ra_astrom[2][:1] == ra_jpl[2][:1] and dec_astrom[2][:1] == dec_jpl[2][:1]:
					break
	else:
		#raise RuntimeError('No match for the asteroid found in {}!'.format(file))
		print 'Target Not Found', file
		os.chdir(cwd)
		continue
	
	return ra_astrom,dec_astrom

def get_fwhm(fits,ra,dec):
	ra = ':'.join(ra)
	dec = ':'.join(dec)
	
	fwhm = subprocess.check_output(['/home/astrolab/matt_laurence/get_fwhm.sh',fits,ra,dec])
	
	return fwhm