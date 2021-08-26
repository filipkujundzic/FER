#include <stdio.h>
#define MIN 100
#define MAX 999

int main(void)
{
    int n,n1=0,t;
    int p=100;
    do{
        scanf("%d",&n);
    }while(n<MIN && n>MAX);
    t=n;
    while(n)
    {
        n1+=n%10*p;
        n/=10;
        p/=10;
    }
    printf("Broj %d %s je od ucitanog broja.",n1,(n1>t)?("veci"):("manji"));
    return 0;
}
