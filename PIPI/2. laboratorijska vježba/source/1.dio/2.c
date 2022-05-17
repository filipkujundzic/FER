#include <stdio.h>

int main(void)
{
    char a[65];
    int i;
    gets(a);
    if(strlen(a)<10)
    {
        printf("Prekratak niz");
        return;
    }
    for(i=0;i<strlen(a);i+=2)
    {
        if(a[i]>='a' && a[i]<='z') printf("%c\n",a[i]);
    }
    return 0;
}
