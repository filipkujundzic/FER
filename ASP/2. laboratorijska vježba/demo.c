#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "datoteka.h"


int brojDatoteka(char *mapa){
	int br;
	Datoteka *popisDatoteka;
	int broj, i;

	broj=vratiDatoteke(mapa, &popisDatoteka);			/* pozovi funkciju koja vraca sve datoteke iz foldera nazivFoldera */
	br=0;												/* ukupni brojac datoteka */
	for (i=0;i<broj;i++){								/* ako je broj>0 onda se ima sta gledati ... */
		if (popisDatoteka[i].vrsta=='F') br++;			/* ako je vrsta datoteke 'F' (file), onda povecaj brojac */
		else 
			br+=brojDatoteka(popisDatoteka[i].putanja); /* a ako nije, onda pogledaj koliko ima datoteka u tom folderu... */
	}
	free(popisDatoteka);								/* oslobadjam zauzetu memoriju... */
	return br;											/* vracam broj datoteka iz foldera mapa */
}


int main(){
	char naziv[] = "G:/D01"; /* / D01 / D0102"; */
	int broj, i;
	Datoteka *poljeDatoteka = NULL;

	broj=vratiDatoteke(naziv,&poljeDatoteka);
	printf("\n Datoteke u mapi \"%s\" :\n",naziv);
	if (broj>0){
		for(i=0;i<broj;i++)
			printf("%2c %-10d %-40s\n", poljeDatoteka[i].vrsta,poljeDatoteka[i].velicina,poljeDatoteka[i].putanja);
		free(poljeDatoteka);
	}

	printf("\nU %s nalazi se %d datoteka\n", naziv, brojDatoteka(naziv));
	return 0;
}





	