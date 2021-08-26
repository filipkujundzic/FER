#include <stdio.h>
#define MAKS 101

int main(void)
{
    int n,br=0,i,k=1;
    int niz[MAKS]={0};
    int najveci[2];
    do{
        scanf("%d",&n);
        if(n>=0 && n<=100) niz[n]++;
        br++;
        if((!(n>=0 && n<=100)) && br<=2)
        {
            printf("Nije uneseno dovoljno brojeva iz trazenog intervala.");
            return 0;
        }
    }while(n>=0 && n<=100);
    for(i=MAKS;i>0;i--)
    {
        if(niz[i]>=2 && k==1)
        {
            najveci[0]=i;
            najveci[1]=i;
            break;
        }
        if(niz[i]>=1)
        {
            najveci[k]=i;
            k--;
        }
        if(k==-1) break;
    }
    printf("Ostatak pri dijeljenju %d sa %d je %d.",najveci[1],najveci[0],najveci[1]%najveci[0]);
    return 0;
}
