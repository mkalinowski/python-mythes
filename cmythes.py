#!/usr/bin/env python3

from ctypes import byref, cdll, c_char_p, c_int, POINTER, Structure
import sys


class MyThes(object):

    lib = cdll.LoadLibrary('./libcmythes.so')

    class mentry(Structure):
        # memory representation of a transparent lib struct
        _fields_ = [('defn', c_char_p),
                    ('count', c_int),
                    ('phyns', POINTER(c_char_p))]

        def to_dict(self):
            return {'defn': self.defn,
                    'count': self.count,
                    'syns': [self.phyns[i] for i in range(self.count)]}

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

    def lookup(self, text):

        # mentry pointer. initialized to NULL
        mentry_p = POINTER(self.mentry)()

        mentries = []
        count = self.lib.MyThes_Lookup(self.obj, c_char_p(text),
                                       c_int(len(text)), byref(mentry_p))
        for i in range(count):
            mentry = mentry_p[i]
            mentries.append(mentry.to_dict())

        self.lib.MyThes_CleanUpAfterLookup(self.obj, byref(mentry_p), count)
        return mentries

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: " + sys.argv[0] +
              " <idx file path> <dat file path> <phrase>")
        quit(-1)

    idxpath = sys.argv[1]
    datpath = sys.argv[2]

    thesaurus = MyThes(idxpath, datpath)
    encoding = thesaurus.get_th_encoding()

    text = " ".join(sys.argv[3:]).encode(encoding)

    synonyms = thesaurus.lookup(text)

    for i, synonym in enumerate(synonyms):
        print("%d. %s" % (i + 1, synonym['defn'].decode(encoding)))

        for w in map(lambda x: x.decode(encoding), synonym['syns'][1:]):
            print("\t%s" % w)
