python-mythes
=============

Python bindings to the libmythes C++ library.
Written as a study of python's ctypes.

To use the library, you have to compile C-C++ glue first. It's needed because
ctypes can't use C++ ABI:
    make 

cmythes.py looks for libcmythes.so you've just created in LD_LIBRARY_PATH, so you'll have to provide the path to libcmythes.so directly (paths can be different on your system):

    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd` python cmythes.py /usr/share/mythes/th_en_US_v2.idx /usr/share/mythes/th_en_US_v2.dat bar


To use thesaurus comfortably from command line, move libcmythes.co and
cmythes.py to /usr/local/lib and create the helper in /usr/local/bin:
    # cat /usr/local/bin/thesaurus
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin /usr/local/lib/cmythes.py /usr/share/mythes/th_en_US_v2.idx /usr/share/mythes/th_en_US_v2.dat $*
    # thesaurus moving picture
    1. (noun) movie
        film
        picture
        moving-picture show
        motion picture
        motion-picture show
        picture show
        pic
        flick
        show (generic term)

Requirements:
* python3
* libmythes
* c++ compiler
