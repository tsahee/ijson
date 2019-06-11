#!/bin/bash
#
# Build MacOS binary wheels based on a local macports installation of yajl
#
# Contributed by Rodrigo Tobar <rtobar@icrar.org>
#
# ICRAR - International Centre for Radio Astronomy Research
# (c) UWA - The University of Western Australia, 2019
# Copyright by UWA (in the framework of the ICRAR)
#

# This assumes yajl is installed using macports, which locally gives us
# a x64-only library (and thus we build an x86-only wheel)
export LDSHARED='gcc -bundle -undefined dynamic_lookup -arch x86_64 -g'
export CFLAGS="-I/opt/local/include"
export LDFLAGS="-L/opt/local/lib"

prefix=/Library/Frameworks/Python.framework/Versions
for python in $prefix/?.?/bin/python{2,3}; do
	$python setup.py bdist_wheel --plat-name macosx_10_6_x86_64
done
delocate-wheel -w wheelhouse dist/*.whl
