#!/usr/bin/env python

from ctypes import cdll, c_char_p
import sys


class MyThes(object):

    lib = cdll.LoadLibrary('./libcmythes.so')

    def __init__(self, idxpath, datpath):

        # C functions require ASCII, but Python 3 strings are UTF-8
        if isinstance(idxpath, str):
            idxpath = idxpath.encode('utf-8', 'surrogateescape')
        if isinstance(datpath, str):
            datpath = datpath.encode('utf-8', 'surrogateescape')

        self.obj = self.lib.MyThes_new(c_char_p(idxpath), c_char_p(datpath))

    def __del__(self):
        self.lib.MyThes_del(self.obj)

    def get_th_encoding(self):
        fun = self.lib.MyThes_get_th_encoding
        fun.restype = c_char_p
        return fun(self.obj).decode('latin1')

if __name__ == "__main__":
    idxpath = "/usr/share/mythes/th_en_US_v2.idx"
    datpath = "/usr/share/mythes/th_en_US_v2.dat"

    thesaurus = MyThes(idxpath, datpath)
    encoding = thesaurus.get_th_encoding()
    print (encoding)
