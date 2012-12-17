#!/usr/bin/python

import sys

isofluxes = []
isonoises = []
autofluxes = []
autonoises = []

with open(sys.argv[1]) as f:
	for line in f:
		if '#' not in line:
			data = line.split()
			
			#print data
			isofluxes.append(float(data[3]))
			isonoises.append(float(data[4]))
			autofluxes.append(float(data[18]))
			autonoises.append(float(data[19]))

isosnrs = map(lambda x,y: x/y, isofluxes, isonoises)
autosnrs = map(lambda x,y: x/y, autofluxes, autonoises)

n = int(sys.argv[2]) - 1

print 'Isotopal Flux SNR', isosnrs[n]
print 'Auto Flux SNR', autosnrs[n]