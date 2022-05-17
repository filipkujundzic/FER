#include <stdio.h>

int main(void)
{
    char oct[6];
    int i,l;
    gets(oct);
    l=strlen(oct);
    for(i=0;i<l;i++)
    {
        if(!(oct[i]>='0' && oct[i]<='8'))
        {
            printf("Ucitani niz nije ispravno zadan.");
            return 1;
        }
    }
    printf("Prva znamenka ucitanog broja je %c.\n",oct[0]);
    printf("Posljednja znamenka ucitanog broja je %c.",oct[l-1]);
    return 0;
}
