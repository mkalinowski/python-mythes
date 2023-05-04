#!/usr/bin/env python3

from ctypes import byref, cdll, c_char_p, c_int, POINTER, Structure
import sys


class MyThes(object):
    """
    MyThes provides an API to libmythes thesaurus.
    """

    lib = cdll.LoadLibrary('libcmythes.so')

    class mentry(Structure):
        # memory representation of a transparent lib struct
        _fields_ = [('defn', c_char_p),
                    ('count', c_int),
                    ('phyns', POINTER(c_char_p))]

        def to_dict(self):
            return {'defn': self.defn,
                    'syns': [self.phyns[i] for i in range(self.count)]}

    def __init__(self, idxpath, datpath):
        """
        idxpath - Thesaurus index, i.e. /usr/share/mythes/th_en_US_v2.idx
        datpath - Thesaurus path, i.e. /usr/share/mythes/th_en_US_v2.dat
        """

        # C functions require ASCII, but Python 3 strings are UTF-8
        if isinstance(idxpath, str):
            idxpath = idxpath.encode('utf-8', 'surrogateescape')
        if isinstance(datpath, str):
            datpath = datpath.encode('utf-8', 'surrogateescape')

        self.obj = self.lib.MyThes_new(c_char_p(idxpath), c_char_p(datpath))

    def __del__(self):
        self.lib.MyThes_del(self.obj)

    def get_th_encoding(self):
        """
        Returns thesaurus encoding. Use this to encode parameters and decode
        return values
        """
        fun = self.lib.MyThes_get_th_encoding
        fun.restype = c_char_p
        encoding = fun(self.obj)
        return encoding.decode('latin1') if encoding else None

    def lookup(self, text):
        """
        Query text should be encoded with encoding returned by
        the `get_th_encoding`.
        Method returns the list of synonyms grouped by the sense. Each synonym
        is a dict with keys:
        defn - sense
        phyns - list of synonyms
        """

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
    if not encoding:
        print("Failed to initialize Thesaurus.")
        quit(-1)

    text = " ".join(sys.argv[3:]).encode(encoding)

    synonyms = thesaurus.lookup(text)

    for i, synonym in enumerate(synonyms):
        print("%d. %s" % (i + 1, synonym['defn'].decode(encoding)))

        for w in map(lambda x: x.decode(encoding), synonym['syns'][1:]):
            print("\t%s" % w)
