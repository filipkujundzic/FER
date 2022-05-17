#include <stdio.h>
#include <stdlib.h>

#define BLOK 4096L
#define N 100000
#define C ((int) (BLOK/sizeof(struct zapis)))
#define M ((int) (N/C*1.3))
#define POCETNA_VRIJEDNOST  9469  //9469 (1) //8249 (6) // 9999 (17) // 7144 (9726) // 8267 (33)
#define MNOZITELJ 63             //63 (1)   // 14 (6)  //  19 (17)  //  40 (9726)  //  29 (33)

struct zapis
{
    char naziv[30+1];
    char ip[15+1];
}domena, in, pretinac[C];

unsigned long Hash(char *niz)
{
    unsigned long hash=POCETNA_VRIJEDNOST;
    char znak;

    while (znak = *niz++)
        hash=MNOZITELJ*hash+znak;

    return hash;
}

int BrojPreljeva(FILE *in)
{
    int i,upisan,preljev,poc;
    int br_preljeva = 0;
    int *polje;

    polje = (int*) calloc(M,sizeof(int));
    fseek(in, 0L, SEEK_SET);

    while (fscanf (in, "%s %s", domena.naziv, domena.ip) != EOF)
    {
        i = Hash(domena.naziv) % M;
        poc = i;
        upisan = 0;
        preljev = 0;
        do{
            if (polje[i] < C){
                polje[i]++;
                if (preljev == 1) br_preljeva++;
                upisan = 1;
            }
            if (upisan) break;

            i = (i + 1) % M ;
            preljev = 1;

        } while( i != poc);
          if ( (i == poc) && (upisan == 0) ) return -1;
    }
    free(polje);
    return br_preljeva;
}

int Upis(struct zapis in, FILE *fhashTablica)
{
    int i,k,poc;
    i = Hash(in.naziv) % M;
    poc = i;
    do{
       fseek(fhashTablica, i*BLOK, SEEK_SET);
       fread (pretinac, sizeof(pretinac), 1, fhashTablica);
       for (k = 0; k < C; k++){
            if(pretinac[k].naziv[0] != '\0')
            {
                if (strcmp (pretinac[k].naziv, in.naziv) == 0)
                {
                    return 1;
                }
            }
            else
            {
                pretinac[k] = in;
                fseek (fhashTablica, i*BLOK, SEEK_SET);
                fwrite(pretinac, sizeof(pretinac), 1, fhashTablica);
                return 1;
            }
       }
       i = (i+1) %M ;
    } while(i!= poc);

return 0;
}

int main(void){
    FILE* du;
    FILE* di;

    du = fopen("domene.txt", "r");
        if (du == NULL) printf("Ne mogu otvoriti ulaznu datoteku \"domene.txt\".");
    di = fopen("binarna.dat", "w+b");
        if (di == NULL) printf("Ne mogu otvoriti izlaznu datoteku \"binarna.dat\".");

    while (fscanf (du,"%s %s",in.naziv,in.ip)!=EOF)
    {
        if(!Upis(in,di)) printf("Tablica puna. Nema mjesta za daljnji upis.");
    }
    printf("Uspjesno je obavljen zapis u Hash tablicu!\n");
    printf("Broj ocekivanih preljeva s konstantama\nPOCETNA VRIJEDNOST = %d i MNOZITELJ = %d: %d", POCETNA_VRIJEDNOST, MNOZITELJ, BrojPreljeva(du));

    fclose(du);
    fclose(di);
return 0;
}
