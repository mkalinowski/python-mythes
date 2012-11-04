#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cmythes.h"

void print_definitions(mentry *entries, int nentries)
{
    for (int i = 0; i < nentries; i++) {
        mentry e = entries[i];

        printf("%d. %s:\n", i + 1, e.defn);

        for (int j = 0; j < e.count; j++) {
            printf("\t%s", e.psyns[j]);
        }
    }
}

void lookup(const char *searchString)
{
    // TODO: extract following dirs
    const char *datpath = "/usr/share/mythes/th_en_US_v2.dat";
	const char *idxpath = "/usr/share/mythes/th_en_US_v2.idx";

	MyThes *thesaurus = MyThes_new(idxpath, datpath);

    int len = strlen(searchString);
    int nentries = 0;
    mentry *entries = NULL;

    nentries = MyThes_Lookup(thesaurus, searchString, len, &entries);

    print_definitions(entries, nentries);

    MyThes_CleanUpAfterLookup(thesaurus, &entries, nentries);

    MyThes_del(thesaurus);
}

int main (int ac, char **av)
{
    if (ac < 2) {
        printf("Usage: %s <word or phrase>", av[0]);
        return (-1);
    }

    // concat all arguments into a single string
    char *all_args, *pargs;
    size_t argslen = 0;

    for (int i = 1; i < ac; i++) {
        argslen += strlen(av[i]);
    }
    argslen += (ac - 1); // account for spaces

    all_args = pargs = (char *) malloc(argslen);

    for (int i = 1; i < ac; i++) {
        int arglen = strlen(av[i]);
        memcpy(pargs, av[i], arglen);
        pargs += arglen + 1;
        *(pargs - 1) = ' ';
    }

    *(pargs - 1) = 0;


    lookup(all_args);
}

