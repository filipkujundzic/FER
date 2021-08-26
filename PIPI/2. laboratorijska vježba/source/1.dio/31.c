#include <stdio.h>

int main(void)
{
    char s[31],s1[31];
    int i;
    gets(s);
    for(i=0;i<strlen(s);i++)
    {
        if(!(s[i]>='a' && s[i]<='z' || s[i]>='A' && s[i]<='Z' || s[i]>='0' && s[i]<='9'))
        {
            printf("Ucitani niz nije ispravno zadan.");
            return 0;
        }
    }
    for(i=0;i<strlen(s);i++)
    {
        s1[i]=s[i];
        if(s1[i]=='a') s1[i]='9';
        if(s1[i]=='e') s1[i]='8';
        if(s1[i]=='i') s1[i]='7';
    }
    s1[strlen(s)]='\0';
    puts(s1);
    return 0;
}
