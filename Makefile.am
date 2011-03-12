ACLOCAL_AMFLAGS = -I m4 --install

SUBDIRS = man resources src data
bin_SCRIPTS = openracing monodevelop.sh
EXTRA_DIST = openracing.in autogen.sh monodevelop.sh.in

REWRITE = \
        sed -e "s|\@prefix\@|$(prefix)|g"               \
            -e "s|\@pkglibdir\@|$(pkglibdir)|g"         \
            -e "s|\@bindir\@|$(bindir)|g"		\
            -e "s|\@ogredotnet_lib\@|$(ogredotnet_lib)|g"		\
            -e "s|\@myguinet_lib\@|$(myguinet_lib)|g"		\
            -e "s|\@tao_lib\@|$(tao_lib)|g"		\
	    -e "s|\@MONO\@|$(MONO)|g" 

openracing: $(top_srcdir)/openracing.in Makefile
	$(REWRITE) $(top_srcdir)/openracing.in > $@.tmp
	mv $@.tmp $@
	chmod +x openracing

monodevelop.sh: $(top_srcdir)/monodevelop.sh.in Makefile
	$(REWRITE) $(top_srcdir)/monodevelop.sh.in > $@.tmp
	mv $@.tmp $@
	chmod +x monodevelop.sh
