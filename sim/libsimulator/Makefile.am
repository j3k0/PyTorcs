SUBDIRS = tgf txml simuv2 plib interfaces
# robottools solid-2.0 

EXTRA_DIST = includes/3D/Basic.h includes/3D/Matrix.h includes/3D/Point.h includes/3D/Quaternion.h includes/3D/Tuple3.h includes/3D/Tuple4.h includes/3D/Vector.h  math/misc.h math/linalg_t.h math/straight2_t.h math/v2_t.h math/v3_t.h math/v4_t.h 
# includes/SOLID/solid.h

pkglib_LTLIBRARIES = libsimulator.la
libsimulator_la_SOURCES = libsimulator.cpp
# libsimulator_la_LIBADD = track/libtrack.la tgf/libtgf.la robottools/librobottools.la txml/libtxml.la drivers/libdrivers.la drivers/olethros/libolethros.la simuv2/libsimuv2.la solid-2.0/libsolid.la learning/liblearning.la plib/libplib.la gnulinux/libgnulinux.la ../swigtorcs/libswigtorcs.la solid-2.0/libsolid.la 
libsimulator_la_LIBADD = tgf/libtgf.la txml/libtxml.la simuv2/libsimuv2.la plib/libplib.la ../swigtorcs/libswigtorcs.la
libsimulator_la_LDFLAGS = -ldl $(OIS_LIBS) $(MYGUI_LIBS) $(STLPORT_LIBS) $(FT2_LIBS) $(OGRE_LIBS)

# CXXLINK = $(LIBTOOL) --tag=CXX --mode=link $(CXXLD) $(AM_CXXFLAGS) $(CXXFLAGS) $(AM_LDFLAGS) $(LDFLAGS) -o $@
