BUILT_SOURCES = swigtorcs.cpp
SWIG_SOURCES = swigtorcs.i swigcar.i swiggfparm.i swiggraphic.i swigmath.i swigraceman.i swigrobot.i swigrobottools.i swigsimu.i swigtrack.i
CLEANFILES = $(srcdir)/swigtorcs.cpp $(srcdir)/*.cs

noinst_LTLIBRARIES = libswigtorcs.la
libswigtorcs_la_SOURCES = $(SWIG_SOURCES) $(BUILT_SOURCES)
INCLUDES = -I@top_srcdir@/src/libsimulator -I@top_srcdir@/src/libsimulator/interfaces

$(srcdir)/swigtorcs.cpp:$(SWIG_SOURCES)
	$(SWIG) -Wall -csharp -namespace SwigTorcs -I$(top_srcdir)/src/libsimulator/interfaces -I$(top_srcdir)/src/libsimulator -I$(srcdir) -outdir $(srcdir) -dllimport libsimulator -o $(srcdir)/swigtorcs.cpp $(srcdir)/swigtorcs.i
