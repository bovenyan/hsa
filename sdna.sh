#!/bin/sh
cd hsa-python
./setup.sh
cd ../hassel-c/
make
./gen stanford
