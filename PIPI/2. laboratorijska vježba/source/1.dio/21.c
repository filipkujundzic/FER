#include <stdio.h>
#define MIN 1
#define MAX 99999

int main(void)
{
    int n,n1,suma=0,i;
    int niz[10]={0};
    do{
        scanf("%d",&n);
    }while(n<MIN || n>MAX);
    n1=n;
    while(n)
    {
        niz[n%10]++;
        n/=10;
    }
    for(i=0;i<10;i++)
    {
        if(niz[i]==1) suma+=i;
    }
    printf("Broj %d - suma znamenaka koje se jednom pojavljuju: %d",n1,suma);
    return 0;
}
