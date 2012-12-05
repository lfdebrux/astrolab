def ra2hr(ra):
	return dec2deg(ra)

def ra2deg(ra):
	return 15*ra2hr(ra)

def dec2deg(dec):
	return sum(map(lambda x,y: float(x)/float(y), dec, (1, 60, 3600)))

def delta_ra(ra1,ra2):
	ra_delta = map(lambda x,y: float(x)-float(y), ra1, ra2)
	return ra2deg(ra_delta)

def delta_dec(dec1,dec2):
	dec_delta = map(lambda x,y: float(x)-float(y), dec1, dec2)
	return dec2deg(dec_delta)

def cleanup(dir):
	subprocess.call("shopts -s extglob; rm -f !(ad*.fits) " + dir, shell=True)