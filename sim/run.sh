#!/bin/bash

cd `dirname $0`
. config-`uname -n`
export PYTHONPATH=`pwd`
export SIMPATH=`pwd`

cd ../data

$PYTHON $SIMPATH/Main.py
