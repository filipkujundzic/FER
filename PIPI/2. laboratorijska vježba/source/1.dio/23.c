#include <stdio.h>

int main(void)
{
    char bin[11];
    int i,p=0;
    gets(bin);
    for(i=0;i<strlen(bin);i++)
    {
        if(bin[i]!='0' && bin[i]!='1')
        {
            printf("Ucitani niz nije ispravno zadan.");
            exit(1);
        }
    }
    for(i=1;i<strlen(bin);i++)
    {
        if(bin[i]=='0' && bin[i-1]=='0')
        {
            p=1;
            break;
        }
    }
    printf("Ucitani binarni broj %s dvije ili vise uzastopnih znamenki 0.",(p==1)?("sadrzi"):("ne sadrzi"));
    return 0;
}
