#include <stdio.h>

int main(void)
{
    int n,i=0,k,br=0;
    int niz1[31]={0},niz2[31];
    while(1==1)
    {
        scanf("%d",&n);
        if(n>=1 && n<=30) br++;
        if(niz1[n]==1)
        {
            for(k=0;k<i;k++)
            {
                if(niz2[k]==n)
                {
                    i++;
                    printf("\nBroj %d bio je %d. ucitani broj.",n,k);
                    printf("\nUkupno ucitano brojeva %d",br);
                }
            }
            break;
        }
        niz1[n]++;
        niz2[i]=n;
        i++;
    }
    return 0;
}
