#include <stdio.h>
#define MIN 1
#define MAX 99999

int main(void)
{
    int n,n1,prva,zadnja;
    do{
        scanf("%d",&n);
    }while(!(n>=MIN && n<=MAX));
    n1=n;
    zadnja=n%10;
    while(n>0)
    {
        prva=n%10;
        n/=10;
    }
    if(prva!=zadnja) printf("Broj %d: prva znamenka je %s od zadnje",n1,(prva>zadnja)?("veca"):("manja"));
    else printf("Broj %d: prva i zadnja znamenka su jednake",n1);
    return 0;
}
