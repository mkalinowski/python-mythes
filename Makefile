CC = clang++

all: libcmythes.so

cmythes.o: cmythes.cpp
	$(CC) -c -fPIC -o cmythes.o cmythes.cpp 

libcmythes.so: cmythes.o
	$(CC) `pkg-config --libs mythes` -shared -Wl,-soname,libcmythes.so -o libcmythes.so cmythes.o

clean:
	rm *.o *.so
