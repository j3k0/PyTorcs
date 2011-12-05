CPP_SOURCES="libsimulator.cpp plib/sg.cpp simuv2/aero.cpp simuv2/axle.cpp simuv2/brake.cpp simuv2/car.cpp simuv2/categories.cpp simuv2/collide.cpp simuv2/differential.cpp simuv2/engine.cpp simuv2/simu.cpp simuv2/simuitf.cpp simuv2/steer.cpp simuv2/susp.cpp simuv2/transmission.cpp simuv2/wheel.cpp tgf/directory.cpp tgf/hash.cpp tgf/module.cpp tgf/os.cpp tgf/params.cpp tgf/profiler.cpp tgf/tgf.cpp tgf/trace.cpp txml/xml.cpp"

C_SOURCES="txml/gennmtab.c txml/hashtable.c txml/xmlparse.c txml/xmlrole.c txml/xmltok.c"

SRCDIR=`pwd`
cd ../build

for i in $C_SOURCES
do
	echo "C $i"
	gcc -arch i386 -fpic -I../libsimulator/interfaces -I../libsimulator -I.. -c $SRCDIR/$i 2> /dev/null
done

for i in $CPP_SOURCES
do
	echo "C $i"
	g++ -arch i386 -fpic -I../libsimulator/interfaces -I../libsimulator -I.. -c $SRCDIR/$i 2> /dev/null
done

