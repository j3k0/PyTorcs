#!/bin/bash

cd `dirname $0`

. config-`uname -n`

export PYTHONPATH=`pwd`
$PYTHON Main.py
