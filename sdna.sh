#!/bin/sh
export PYTHONPATH=$PYTHONPATH:~/hassel-public/hsa-python
cd hsa-python
./setup.sh
cd examples/stanford
mkdir tf_stanford_backbone
python generate_stanford_backbone_tf.py
cd ../../../hassel-c/
make
./clean.sh
