#!/bin/bash

main_dir=`pwd`
fcc_dir="FCCAnalyses"

#cd /afs/cern.ch/work/y/yborysen/private/ALPs/

cd $fcc_dir
rm -r install build
source setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install