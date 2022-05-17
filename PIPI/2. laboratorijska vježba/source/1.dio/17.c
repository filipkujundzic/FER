#include <stdio.h>

int main(void)
{
    int i,br=0;
    char a[30],b[30];
    gets(a);
    gets(b);
    for(i=0;i<strlen(a);i++)
    {
        if(i%2==0)
        {
            a[i]=b[i];
            br++;
        }
    }
    puts(a);
    printf("Broj promijenjenih znakova: %d",br);
    return 0;
}
