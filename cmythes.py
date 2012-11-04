#!/usr/bin/env python2

from ctypes import cdll, c_char_p
import sys


class MyThes(object):

    lib = cdll.LoadLibrary('./libcmythes.so')

    def __init__(self, idxpath, datpath):

        self.obj = self.lib.MyThes_new(c_char_p(idxpath), c_char_p(datpath))

    def __del__(self):
        self.lib.MyThes_del(self.obj)

if __name__ == "__main__":
    idxpath = b"/usr/share/mythes/th_en_US_v2.idx"
    datpath = b"/usr/share/mythes/th_en_US_v2.dat"

    thes = MyThes(idxpath, datpath)
