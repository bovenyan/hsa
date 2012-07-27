#!/bin/bash
python setup.py build
cp build/lib.*/c_wildcard.so ../hsa-python/utils/.
