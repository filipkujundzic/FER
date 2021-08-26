#include <stdio.h>

int main(void)
{
    int niz[10]={0};
    int a,i;
    do{
        scanf("%d",&a);
    }while(!(a>=100 && a<=99999));
    while(a>0)
    {
        niz[a%10]++;
        a/=10;
    }
    for(i=0;i<10;i++)
    {
        if(niz[i]!=0) printf("znamenka %d : %d\n",i,niz[i]);
    }
    return 0;
}
