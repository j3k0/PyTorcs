mkdir -p build
rm -f build/*.o

DIRS="libsimulator swigtorcs"
for i in $DIRS
do
	cd $i
	./compile.sh
	cd ..
done

g++ -arch i386 -shared -ldl -lpython2.6 build/*.o -o libsimulator.so
