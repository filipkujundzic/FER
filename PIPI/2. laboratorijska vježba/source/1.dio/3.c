#include <stdio.h>

int main(void)
{
    char s[60];
    int i;
    scanf("%s",s);
    if(strlen(s)-1<10)
    {
        printf("Prekratak niz");
        return;
    }
    for(i=strlen(s)-1;i>=0;i--)
    {
        if(s[i]>='A' && s[i]<='Z' || s[i]>='0' && s[i]<='9')
        printf("%c\n",s[i]);
    }
    return 0;
}
