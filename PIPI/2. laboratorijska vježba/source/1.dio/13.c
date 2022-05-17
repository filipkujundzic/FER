#include <stdio.h>

int main(void)
{
    int n,i;
    int niz[31]={0};
    do{
        scanf("%d",&n);
        niz[n]++;
    }while(n>=1 && n<=30);
    printf("\n");
    for(i=0;i<31;i++)
    {
        if (niz[i]>1) printf("Broj %d: %d\n",i,niz[i]);
    }
    return 0;
}
