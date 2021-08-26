#include <stdio.h>

int main(void)
{
    int niz[1000];
    int n,i;
    double rez=0;
    do{
        scanf("%d",&n);
    }while(n<1 || n>1000);
    for(i=1;i<=n;i++)
    {
        rez+=1./((2*i-1)*(2*i+1));
    }
    printf("Rezultat pomocu parcijalne sume: %lf\n",rez);
    (rez-0.5>0) ? printf("Apsolutna vrijednost pogreske: %lf",rez-0.5) : printf("Apsolutna vrijednost pogreske %lf",(rez-0.5)*-1);
    return 0;
}
