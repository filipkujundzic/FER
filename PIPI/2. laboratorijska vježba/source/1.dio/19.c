#include <stdio.h>
#define MIN 100
#define MAX 99999

int main(void)
{
    int niz[10]={0};
    int a,i,a1;
    do{
        scanf("%d",&a);
    }while(!(a>=MIN && a<=MAX));
    a1=a;
    while(a>0)
    {
        niz[a%10]++;
        a/=10;
    }
    for(i=9;i>=0;i--)
    {
        if(niz[i]!=0)
        {
            printf("U broju %d najveca znamenka je %d.",a1,i);
            break;
        }
    }
    return 0;
}
