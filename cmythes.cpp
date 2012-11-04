#include <stdio.h>
#include <mythes.hxx>
extern "C" {

    MyThes *MyThes_new(const char *idxpath, const char *datpath)
    {
        return new MyThes(idxpath, datpath);
    }

    void MyThes_del(MyThes *instance)
    {
        delete instance;
    }

    int MyThes_Lookup(MyThes *instance, const char *pText, int len,
                      mentry **pme)
    {
        return instance->Lookup(pText, len, pme);
    }

    void MyThes_CleanUpAfterLookup(MyThes *instance, mentry **pme, int nmean)
    {
        instance->CleanUpAfterLookup(pme, nmean);
    }

    char *MyThes_get_th_encoding(MyThes *instance)
    {
        return instance->get_th_encoding();
    }
}
