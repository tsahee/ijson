#!/bin/bash
#
# Build manylinux binary wheels using a manually compiled yajl install
# within the quay.io/pypa/manylinux1_x86_64 docker container
#
# Run like: docker run -v $PWD:/io quay.io/pypa/manylinux1_x86_64 bash /io/linux-wheels.sh
#
# Contributed by Rodrigo Tobar <rtobar@icrar.org>
#
# ICRAR - International Centre for Radio Astronomy Research
# (c) UWA - The University of Western Australia, 2019
# Copyright by UWA (in the framework of the ICRAR)
#

copy_or_get() {
	name="$1"
	url="$2"
	if [ -f /io/"$name" ]; then
		cp /io/"$name" .
	else
		curl -L -o "$name" "$url"
	fi
}

cd /tmp
copy_or_get cmake-3.1.3-Linux-x86_64.sh https://cmake.org/files/v3.1/cmake-3.1.3-Linux-x86_64.sh
copy_or_get yajl-2.1.0.tar.gz https://github.com/lloyd/yajl/archive/2.1.0.tar.gz

# Unpack cmake and use it to install yajl
yes | sh cmake-3.1.3-Linux-x86_64.sh
rm cmake-3.1.3-Linux-x86_64.sh
CMAKE="`pwd`/cmake-3.1.3-Linux-x86_64/bin/cmake"
tar xf yajl-2.1.0.tar.gz
cd yajl-2.1.0; mkdir build; cd build
${CMAKE} .. -DCMAKE_C_FLAGS="-O3"
make all -j 4
make install

# build wheels
for PY in /opt/python/*/bin; do
	CFLAGS="-O3" ${PY}/pip -v wheel /io/ -w wheelhouse/
done
for w in wheelhouse/*.whl; do
	auditwheel repair $w -w /io/wheelhouse
done
