#include <stdio.h>

int main(void)
{
    int a,niz[61]={0};
    int br=0;
    while(1==1)
    {
        scanf("%d",&a);
        if(!(a>=-30 && a<=30))
        {
            printf("Pogresan broj!");
            return 0;
        }
        niz[30+a]++;
        if(niz[30+a]==3)
        {
            br++;
            break;
        }
        br++;
    }
    printf("\nUkupno je ucitano %d brojeva.",br);
    return 0;
}
