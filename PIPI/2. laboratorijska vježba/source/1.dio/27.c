#include <stdio.h>

int main(void)
{
    int niz[101]={0};
    int i,a,p=0,najmanji,najveci;
    do{
        scanf("%d",&a);
        if(niz[a]==0) niz[a]++;
    }while(a>=0 && a<=100);
    for(i=0;i<101;i++)
    {
        if(niz[i]==1) p=1;
    }
    if(p==0)
    {
        printf("Nije unesen niti jedan broj iz trazenog intervala.");
        return 0;
    }
    for(i=0;i<101;i++)
    {
        if(niz[i]==1 && i%4==0)
        {
            najmanji=i;
            break;
        }
    }
    for(i=101;i>0;i--)
    {
        if(niz[i]==1 && i%4==0)
        {
            najveci=i;
            break;
        }
    }
    printf("Zbroj namanjeg (%d) i najveceg (%d) broja djeljivog s 4 je %d.",najmanji,najveci,najmanji+najveci);
    return 0;
}
