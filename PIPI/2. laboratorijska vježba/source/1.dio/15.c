#include <stdio.h>

int main(void)
{
    int a,br=0,i;
    int niz[41]={0};
    do{
        scanf("%d",&a);
        br++;
        if(niz[a]==0) niz[a]=br;
    }while(a>=1 && a<=40);

    for(i=1;i<=41;i++)
    {
        if(niz[i]!=0)
            printf("Broj %2d : %2d\n",i,niz[i]);
    }
    return 0;
}
