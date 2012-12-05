import sys,os,subprocess
import argparse

parser = argparse.ArgumentParser(description="Copy files from archive that are listed in a csv")

parser.add_argument('csv', help='a csv file containing the list of images to copy')
parser.add_argument('root', metavar='dest', help='the folder to copy files into')

parser.add_argument('--pretend', dest='pretend', action='store_true', help='output files to be copied instead of copying')
parser.add_argument('--observer', dest='this_observer', default='Matt+Laurence', help='copy only files taken by a particular observer')
parser.add_argument('--ignore-usable', dest='usable', action='store_false', help='get files even if marked as unusable')
#parser.add_argument('--ignore-astrometry', dest='astrom', action='store_true', help='get file even if there is no astrometry on it')

args = parser.parse_args()

log = open(args.csv)

log.readline() # skip header line

#os.chdir('/remote/archive')

#print os.getcwd()

for line in log:
	# skip bad pictures
	if args.usable and line.split(',')[11] is 'n':
		continue
	# only get pics by us
	if args.this_observer not in line.split(',')[2].strip():
		continue
	
	date,telescope,observer,run,target = [x.strip() for x in line.split(',')[0:5]]
	day,month,year = date.split('/')
	date = '_'.join((year[2:],month,day))
	telescope = telescope.lower()
	run = run.strip()
	
	fits = os.path.join('/remote/archive',telescope,year,date,'ad' + run + '.fits')
	
	# print fits,os.path.isfile(fits)
	
	# copy files, --parent recreates directory structure
	# subprocess.call(["cp","--parent",fits,args.root])
	
	dest = os.path.join(args.root,target,date,'') # split by target and date observed
	
	if args.pretend:
		print fits,"->",dest
	elif not args.pretend:
		if not os.path.isdir(dest):
			os.makedirs(dest)	
		subprocess.call(["cp","--no-clobber",fits,dest])