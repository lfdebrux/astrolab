#!/bin/bash

STARLINK_DIR=${STARLINK_DIR:-/star}

source ${STARLINK_DIR}/etc/profile

# load starlink packages
figaro > /dev/null
convert > /dev/null

# create a display window
#gdset xwindows
#xmake xwindows -width 800 -height 600
idev xw

for fits in "$@"
do
	echo $fits

	# display image
	#display $fits noaxes mode=faint clear=true > /dev/null
	image $fits erase=true accept > /dev/null

	# query user
	read -n1 -p 'Keep? [Y/n]: ' keep
	echo

	# mark if 'n'
	if [ $keep = 'n' ]
	then
		mv $fits ${fits}.no
	fi
done