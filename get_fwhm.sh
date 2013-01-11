#!/bin/sh

STARLINK_DIR=${STARLINK_DIR:-/star}

source ${STARLINK_DIR}/etc/profile

fits=$1
ra=$2
dec=$3

base="`basename "$fits" .fits`"
ndf=${base}.sdf

# load necessary packages
convert > /dev/null
kappa > /dev/null

# convert file to ndf
fits2ndf $fits $ndf

# convert position to expected format
#listmake ${base}_pos.txt ndf=$ndf mode="Interface" position="$ra $dec"

# put positions in a file
echo $ra $dec > pos.txt

# find psf
psf $ndf incat=! device=! cofile=pos.txt > /dev/null

parget fwhm psf

rm pos.txt $sdf

