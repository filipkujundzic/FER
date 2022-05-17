#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int br;

char *povezi(void)
{
    int i;
    char in[20+1];
    char* out;
    int l=0;

    out=(char *) malloc (sizeof (char) );
    out[0]='\0';

    for(i=1;i>0;i++)
    {
        printf ("Unesite %d. niz: ",i);
        gets(in);
        if (in[0] == '.' && in[1] == '\0')
        {
            br=i;
            break;
        }
        if ( strlen(in) > 20 )
        {
            printf("Niz je pogresno unesen, veci je od 20 znakova.\nZavrsetak programa.\n");
            exit (1);
        }
        l+=strlen(in);
        out=(char *) realloc(out,(l+1)*sizeof(char));
        strcat(out,in);
    }
    return out;
}

int main(void)
{
    char *s;
    s=povezi();
    printf("\nNiz dobiven povezivanjem %d nizova je: \n",br);
    puts(s);
    free(s);
    return 0;
}
