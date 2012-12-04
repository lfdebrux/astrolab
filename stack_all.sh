#!/usr/bin/bash

start_dir=`pwd`

for dir in "$@"
do
	#echo $dir
	cd $dir
	
	if [ "`ls ad*.fits | wc -l`" -gt "1" ]
	then
		echo $dir start
		/remote/aa_64bin/auto_astrom/register_stack ad > /dev/null
		
		date=`basename $dir`
		asteroid=$(basename $(dirname $dir))
		mv mosaic.fit ${asteroid}_${date}.fits
		echo $dir finished
	fi
	
	cd $start_dir
done