#include <stdio.h>

int main(void)
{
    int n,i,k=0;
    int niz1[15],niz2[15];
    do{
        scanf("%d",&n);
    }while(n<1 || n>15);
    for(i=0;i<n;i++) scanf("%d",&niz1[i]);
    for(i=0;i<n;i++)
    {
        if(niz1[i]>=-10 && niz1[i]<=15)
        {
            niz2[k]=niz1[i];
            k++;
        }
    }
    printf("Novo polje: ");
    for(i=0;i<k;i++) printf("%d ",niz2[i]);
    return 0;
}
