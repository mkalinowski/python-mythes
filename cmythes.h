typedef struct MyThes MyThes;
typedef struct mentry {
    char* defn;
    int count;
    char** psyns;
} mentry;

MyThes* MyThes_new(const char* idxpath, const char* datpath);

void MyThes_del(MyThes* instance);

int MyThes_Lookup(MyThes* instance, const char* pText, int len, mentry** pme);

void MyThes_CleanUpAfterLookup(MyThes* instance, mentry** pme, int nmean);

char* MyThes_get_th_encoding(MyThes* instance);
