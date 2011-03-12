#!/bin/bash
#if test -e configure
#then
#    automake -a && aclocal && autoconf -I m4 && libtoolize --force
#else
    autoreconf --force --install -I config -I m4
#fi
