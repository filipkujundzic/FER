#include <stdio.h>

int main(void)
{
    char hex[11];
    int i,br=0;
    gets(hex);
    for(i=0;i<strlen(hex);i++)
    {
        if(!(hex[i]>='0' && hex[i]<='9' || hex[i]>='a' && hex[i]<='f' || hex[i]>='A' && hex[i]<='F'))
        {
            printf("Ucitani niz nije ispravno zadan.");
            return 0;
        }
    }
    for(i=0;i<strlen(hex);i++) if(hex[i]>='0' && hex[i]<='7') br++;
    printf("Broj unesenih oktalnih znamenki: %d",br);
    return 0;
}
