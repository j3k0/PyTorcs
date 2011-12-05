BUILT_SOURCES="swigtorcs.cpp"
SWIG_SOURCES="swigtorcs.i swigcar.i swiggfparm.i swiggraphic.i swigmath.i swigraceman.i swigrobot.i swigrobottools.i swigsimu.i swigtrack.i"

PYTHON_FLAGS="-I/System/Library/Frameworks/Python.framework/Versions/2.6/include/python2.6 -I/System/Library/Frameworks/Python.framework/Versions/2.6/include/python2.6 -fno-strict-aliasing -fno-common -dynamic -DNDEBUG -g -fwrapv -Os -Wall -Wstrict-prototypes -DENABLE_DTRACE -arch i386"
#python-config --cflags

swig -Wall -python -c++ -I../libsimulator/interfaces -I../libsimulator -I.. -outdir . swigtorcs.i
g++ $PYTHON_FLAGS -I../libsimulator/interfaces -I../libsimulator -I.. -c swigtorcs_wrap.cxx
