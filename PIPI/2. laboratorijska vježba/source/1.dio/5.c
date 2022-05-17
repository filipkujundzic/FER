#include <stdio.h>
#define PI 3.141593

int main(void)
{
    int a[1000];
    int i,k,n;
    double rez=1;
    do{
        scanf("%d",&n);
    }while(n<1 || n>1000);

    for(i=0,k=1;i<n;i++,k+=2) a[i]=k;
   // for(i=0;i<n;i++) printf("%d\n",a[i]);
    for(i=1;i<n;i++)
    {
        if(i%2!=0) rez-=1./a[i];
        else rez+=1./a[i];
        //printf("%lf\n",4*rez);
    }
    rez*=4;
    printf("Parcijalna suma: %lf\n",rez);
    ((PI-rez)<0) ? printf("Apsolutna vrijednost pogreske: %lf",(PI-rez)*-1) :  printf("Apsolutna vrijednost pogreske: %lf",(PI-rez));
    return 0;
}
