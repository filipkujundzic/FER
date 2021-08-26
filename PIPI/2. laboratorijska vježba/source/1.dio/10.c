#include <stdio.h>

int main(void)
{
    int n,i,suma=0;
    int niz[20];
    do{
        scanf("%d",&n);
    }while(n<1 || n>20);
    for(i=0;i<n;i++) scanf("%d",&niz[i]);
    for(i=0;i<n;i++)
    {
        if(niz[i]>=-10 && niz[i]<=10)
        {
            suma+=niz[i];
            niz[i]=0;
        }
    }
    //for(i=0;i<n;i++) printf("%d ",niz[i]); ****Nepotreban ispis u zadatku => dodatna provjera
    printf("\nSuma: %d",suma);
    return 0;
}
