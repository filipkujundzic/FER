#include <stdio.h>

int main(void)
{
    char s[21];
    int i;
    gets(s);
    if(strlen(s)-1<8)
    {
        printf("Prekatak");
        return 0;
    }
    for(i=0;i<strlen(s)-1;i++)
    {
        if(s[i]>='A' && s[i]<='Z') break;
    }
    if(i==strlen(s)-1) printf("Ne sadrzi slovo");
    else printf("Zadovoljava uvjete");
    return 0;
}
