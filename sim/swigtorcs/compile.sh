. ../config-`uname -n`

BUILT_SOURCES="swigtorcs.cpp"
SWIG_SOURCES="swigtorcs.i swigcar.i swiggfparm.i swiggraphic.i swigmath.i swigraceman.i swigrobot.i swigrobottools.i swigsimu.i swigtrack.i"

echo S swigtorcs.i
swig -Wall -python -c++ -I../libsimulator/interfaces -I../libsimulator -I.. -outdir . swigtorcs.i
SRCDIR=`pwd`
cd ../build
echo C swigtorcs_wrap.cxx
g++ $PYTHON_FLAGS -fpic -I../libsimulator/interfaces -I../libsimulator -I.. -c $SRCDIR/swigtorcs_wrap.cxx 2> /dev/null
