#include <stdio.h>
#define MAKS 101

int main(void)
{
    int niz[MAKS]={0};
    int n,i,p=0;
    int suma=0;
    do{
        scanf("%d",&n);
        if(n>=0 && n<=MAKS-1) niz[n]++;
    }while(n>=0 && n<=MAKS-1);
    for(i=0;i<MAKS+1;i++)
    {
        if(niz[i]==1)
        {
            p=1;
            break;
        }
    }
    if(p==0)
    {
        printf("Nije unesen niti jedan broj iz trazenog intervala.");
        return 0;
    }
    for(i=0;i<49;i++)
    {
        if(niz[i]!=0) suma+=i*niz[i];
    }
    printf("Zbroj svih unesenih brojeva manjih od 50 je %d.",suma);
    return 0;
}
