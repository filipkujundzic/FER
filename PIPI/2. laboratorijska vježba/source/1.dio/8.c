#include <stdio.h>

int main(void)
{
    char s[31];
    int i,slova=0,znamenke=0;
    scanf("%s",s);
    for(i=0;i<strlen(s);i++)
    {
        if(s[i]>='a' && s[i]<='z') slova++;
        if(s[i]>='1' && s[i]<='9') znamenke++;
    }
    if(slova>=7 && znamenke>=2) printf("Zadovoljava uvjete");
    else printf("Ne zadovoljava uvjete");
    return 0;
}
