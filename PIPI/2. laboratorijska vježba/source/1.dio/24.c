#include <stdio.h>

int main(void)
{
    int i,br=0;
    char niz[5];
    gets(niz);
    for(i=0;i<strlen(niz);i++)
    {
        if(!(niz[i]>='0' && niz[i]<='8'))
        {
                printf("Ucitani niz nije ispravno zadan.");
                return 0;
        }
    }
    for(i=0;i<strlen(niz);i++)
    {
        if(niz[i]=='4') br++;
    }
    printf("Znamenka 4 se u ucitanom broju pojavljuje %d puta.",br);
    return 0;
}
