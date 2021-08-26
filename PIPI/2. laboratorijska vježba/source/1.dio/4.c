#include <stdio.h>

int main(void)
{
    int n,a[20];
    int i;
    do{
        scanf("%d",&n);
    }while(!(n>=1 && n<=20));

    for(i=0;i<n;i++) scanf("%d",&a[i]);

    for(i=0;i<n;i++)
    {
        if(a[i]>=10 && a[i]<=20) printf("%2d. %d\n",i,a[i]);
    }
    return 0;
}
