def get_number_rms(f):
	s = 0
	
	with open(f) as file:
		for line in file:
			if '1Plate solution: 6-coefficient' in line:
				s = 1
				continue
			if s is 1 and 'n' in line and 'catalogue' in line:
				s = 2
				continue
			if s is 2:
				if 'RMS :' in line:
					astrom_rms = line.split()[4]
					break
				if len(line.split()) > 0:
					#print line.split()
					astrom_number = line.split()[0]
	return astrom_number,astrom_rms

if __name__ == "__main__":
	import sys
	
	print get_number_rms(sys.argv[1])