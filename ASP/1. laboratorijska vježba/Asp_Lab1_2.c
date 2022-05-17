#include <stdio.h>
#include <string.h>

float slicnostNizova(char* niz1, char* niz2, int l)
{
    if (*niz1 == '\0' || *niz2 == '\0') return 0;
    if(*niz1 == *niz2)
    {
        return (2.0 / l + slicnostNizova(++niz1,++niz2,l));
    }
    else
    {
        return slicnostNizova(++niz1,++niz2,l);
    }
}

int main(void)
{
    char s1[20+1],s2[20+1];
    printf("Ispitivanje slicnosti dva niza niza:\n");
    do{
            printf("Prvi niz (ne veci od 20 znakova): ");
            gets(s1);
    }while(strlen(s1)>20);
    printf("Prvi niz uspjesno ucitan!\n");
    do{
            printf("Drugi niz (ne veci od 20 znakova): ");
            gets(s2);
    }while(strlen(s1)>20);
    printf("Drugi niz uspjesno ucitan!\n");
    printf("\nSlicnost nizova je: %f \n",slicnostNizova(s1,s2,strlen(s1)+strlen(s2)));
    return 0;
}
