#include <stdio.h>

int main(void)
{
    char hex[6];
    int i,l;
    char maks;
    gets(hex);
    l=strlen(hex);
    for(i=0;i<l;i++)
    {
        if(!(hex[i]>='0' && hex[i]<='9' || hex[i]>='a' && hex[i]<='e' || hex[i]>='A' && hex[i]<='E'))
        {
            printf("Ucitani niz nije ispravno zadan.");
            return 0;
        }
    }
    maks=hex[0];
    for(i=1;i<l;i++)
    {
        if(hex[i]>maks) maks=hex[i];
    }
    printf("Najveca heksadekadska znamenka u ucianom broju je %c.",maks);
    return 0;
}
