SOURCES="libsimulator.cpp plib/sg.cpp simuv2/aero.cpp simuv2/axle.cpp simuv2/brake.cpp simuv2/car.cpp simuv2/categories.cpp simuv2/collide.cpp simuv2/differential.cpp simuv2/engine.cpp simuv2/simu.cpp simuv2/simuitf.cpp simuv2/steer.cpp simuv2/susp.cpp simuv2/transmission.cpp simuv2/wheel.cpp tgf/directory.cpp tgf/hash.cpp tgf/module.cpp tgf/os.cpp tgf/params.cpp tgf/profiler.cpp tgf/tgf.cpp tgf/trace.cpp txml/xml.cpp"

SRCDIR=`pwd`
cd ../build
for i in $SOURCES
do
	g++ -arch i386 -I../libsimulator/interfaces -I../libsimulator -I.. -c $SRCDIR/$i
done
