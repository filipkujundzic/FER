#include <stdio.h>

int main(void)
{
    char s[20],t;
    int i;
    gets(s);
    for(i=0;i<strlen(s);i++)
    {
        if(s[i]>='a' && s[i]<='z' && s[i]!='\0')
        {
            t=s[i];
            s[i]=s[strlen(s)-1];
            s[strlen(s)-1]=t;
            break;
        }
    }
    puts(s);
    return 0;
}
