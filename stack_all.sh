#!/usr/bin/bash

start_dir=`pwd`

for dir in "$@"
do
	#echo $dir
	cd $dir
	
	if [ "`ls ad*.fits | wc -l`" -gt "1" ]
	then
		echo $dir start
		/remote/aa_64bin/auto_astrom/register_stack ad 2>&1 | tee stack.log > /dev/null
		
		date=$(basename $(pwd))
		asteroid=$(basename $(dirname $(pwd)))
		mv mosaic.fits ${asteroid}_${date}_stacked.fits
		echo $dir finished
	fi
	
	cd $start_dir
done
