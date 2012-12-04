import sys,subprocess,os
from getch import getch

GAIA = '/star-kaulia/bin/gaia/gaia.sh'

for fits in sys.argv[1:]:
	subprocess.call(GAIA+' '+fits,shell=True)
	
	print 'Keep? [Y/n]: ',
	keep = getch()
	print
	
	if 'n' in keep:
		os.rename(fits,fits+'.no')