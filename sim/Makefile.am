SUBDIRS = swigtorcs libsimulator 

openracingdir=$(pkglibdir)
openracing_SCRIPTS = openracing.exe
EXTRA_DIST = $(openracing_sources) $(openracing_sources_in)
CLEANFILES = openracing.exe

include Makefile.sync
# include swigtorcs/Makefile.include

openracing_sources = $(FILES)

openracing_build_sources = $(addprefix $(srcdir)/, $(openracing_sources))

resources = $(srcdir)/../resources/dummy.txt
references = $(REFERENCES) $(DLL_REFERENCES)

embedded= $(foreach res,$(resources), $(addprefix -resource:,$(res)),$(notdir $(res)))
embedded_ref= $(foreach ref,$(references), $(addprefix -reference:,$(ref)))

openracing.exe: $(openracing_build_sources) $(resources)
	$(GMCS) $(GTKSHARP_LIBS) $(embedded) -debug -lib:@tao_lib@ -lib:@ogredotnet_lib@ -lib:@myguinet_lib@ $(embedded_ref) -out:$@ $(openracing_build_sources)
