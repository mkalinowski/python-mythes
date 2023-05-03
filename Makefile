CXX = clang++
CC = clang

all: libcmythes.so

cmythes.o: cmythes.cpp
	$(CXX) -c -fPIC -o cmythes.o cmythes.cpp 

libcmythes.so: cmythes.o
	$(CXX) `pkg-config --libs mythes` -shared -Wl,-soname,libcmythes.so -o libcmythes.so cmythes.o

thesaurus:
	$(CC) --std=c99 -lcmythes -L. -o thesaurus thesaurus.c

clean:
	rm -f *.o *.so
