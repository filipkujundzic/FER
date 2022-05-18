/*
Napredni operacijski sustavi
1. laboratorijska vježba
zadatak 1b
filozofi.c
*/

#define _XOPEN_SOURCE 500
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>

#define MAXMSG 18 // poruka može biti velika najviše 18 znakova
#define BRFILOZOFA_MIN 3 // minimalni dopušteni broj filozofa
#define BRFILOZOFA_MAX 10 // maksimalni dopušteni broj filozofa


int br_filozofa;
char primljeno[MAXMSG] = "";	// poruka koja se prima
char tmp_por[MAXMSG] = "";	// pomocno polje
char poslano[MAXMSG] = ""; /* poruka koja se salje */

int cj[BRFILOZOFA_MAX][BRFILOZOFA_MAX][2]; // inicijalizacija cjevovoda

// ažuriranje sata pojedinog procesa (filozofa)
int updateClock(int x, int y) {
	int rez;
	(x > y) ? (rez = x + 1) : (rez = y + 1);
	return rez;
}


void pospan(int id){	//filozofu je dosadno na konferenciji pa mu se spava
	int spavaj;
	srand(time(NULL) + id); 						// koristim id filozofa da bi dobio što različitije vrijeme
	spavaj = (rand() % (2000 - 100)) + 100; 		// slučajno vrijeme spavanja
	sleep(spavaj/1000); 							// pretvaranje u milisekunde - spavaj x milisekundi
}

void filozof(int fil_ID, int T) {

	int zahtjevi[br_filozofa];
	int drugiId, drugiSat;
	int trenutni_sat = T;
	int novi_sat = trenutni_sat;

	int i, brojac;
	brojac = 0;

	// postavi brojač zahtjeva na nula, zatvori krajeve cjevovoda koje je potrebno zatvoriti
	for(int i = 0; i< br_filozofa; i++) {

		zahtjevi[i] = 0;

        if (fil_ID != i) {
			close(cj[fil_ID][i][0]);
			close(cj[i][fil_ID][1]);
        }	
	}
	
		// Konferencija je, "sudjelujem", a zapravo spavam
		printf("F%d: Sudjelujem na konferenciji\n", fil_ID);
		pospan(fil_ID); // spavaj slučajni broj između 100 i 2000 milisekundi

		// Gladan sam - šaljem zahtjev za stolom (kritični odsječak)
		sprintf(poslano, "Zahtjev(P=%d,T=%2d)", fil_ID, trenutni_sat);
		zahtjevi[fil_ID] = trenutni_sat;
		for(int i = 0; i< br_filozofa; i++) {
			if (i != fil_ID) {	//pazim da ne šaljem samome sebi
				printf("F%d: šaljem F%d   %s\n", fil_ID, i, poslano);
				write(cj[fil_ID][i][1], poslano, strlen(poslano) + 1);
				sleep(1);
			}
		}
		
		sleep(1);
		// Primi zahtjeve, napravi update sata, ako je potrebno odgovori, ako ne, spremi za kasnije
		for (int i = 0; i < br_filozofa; i++) {
	        if (i != fil_ID) {	// ako ovo nije moj cjevovod primi zahtjev
	        	sleep(1);

		        read(cj[i][fil_ID][0], primljeno, MAXMSG); //čitam i pohranjujem u "primljeno"

		        for(int j=0; j<MAXMSG; j++)
		        	tmp_por[j] = primljeno[j]; //radim kopiju

				sscanf(tmp_por, "%*[^0-9]%d%*[^0-9]%d%*[^0-9]", &drugiId, &drugiSat); // izvuci podatke iz privrem. spremnika
	    		printf("F%d: primam   %s\n", fil_ID, primljeno);
				//ažuriraj sat
				novi_sat = updateClock(novi_sat, drugiSat);

		        if (zahtjevi[fil_ID] != 0 && ((trenutni_sat == drugiSat && fil_ID < i) || (trenutni_sat < drugiSat))) {
		            zahtjevi[i] = drugiSat;
		        } 
		        else {
		            sprintf(poslano, "Odgovor(P=%2d,T=%2d)", fil_ID, drugiSat);
	    			printf("F%d: šaljem F%d   %s\n", fil_ID, i, poslano);
					write(cj[fil_ID][i][1], poslano, strlen(poslano));
		        }
		    } 
		}

		// Pričekaj da drugi filozofi pošalju odgovor
		for (int i = 0; i < br_filozofa; i++) {
	        if (i != fil_ID) {	//čekam odgovor od drugih filozofa
	        	sleep(2);

	            read(cj[i][fil_ID][0], primljeno, MAXMSG); 	// pročitaj primljeno
	            
	            for(int j=0; j<strlen(primljeno); j++)
		        	tmp_por[j] = primljeno[j];	//pohrani poruku u privremeni spremnik
		        
	    		sscanf(tmp_por, "%*[^0-9]%d%*[^0-9]%d%*[^0-9]", &drugiId, &drugiSat); // izvuci podatke iz privrem. spremnika
	    		printf("F%d: primam   %s\n", fil_ID, primljeno);	//ispis na output programa
				novi_sat = updateClock(novi_sat, drugiSat);			// ažuriraj sat
	        }
		}

		
		// Ulazak u kritični odsječak (stol)
		printf("\n");

		printf("Filozof %d je za stolom i jede\n\n", fil_ID);
		sleep(3); // spavaj tri sekunde

		// Izađi iz kritičnog odsječka i odgovori na pristigle zahtjeve
		for (int i = 0; i < br_filozofa; i++) {
	        if (i != fil_ID) {		//trebam indekse različite od svoga
	        	if (zahtjevi[i] != 0) { //nema smisla provjeravati zahtjeve ako nisu stigli
	          	 	sprintf(poslano, "Odgovor(P=%2d,T=%2d)", fil_ID, zahtjevi[i]);
	          	 	printf("F%d: gotov KO šaljem F%d   %s\n", fil_ID, i, poslano);	// ispis izlaska iz kritičnog odsječka
					write(cj[fil_ID][i][1], poslano, strlen(poslano));				// odgovor na pristigle zahtjeve
	            	zahtjevi[i] = 0;
	       		}
	       	}
		}

		trenutni_sat = novi_sat;	//postavljanje sata
		brojac++;

		printf("F%d: Sudjelujem na konferenciji\n", fil_ID);
		pospan(fil_ID);			// spavaj između 100 i 2000 milisekundi
	

}
void retreat(int failure) {
    exit(0);
}


int main(void) {

	int i, j;
	char sat;
	srand(time(NULL));

	int pid = getpid();

	//unos broja filozofa - čitanje s tipkovnice
	printf("Unesite broj filozofa: ");
	scanf("%d",&br_filozofa);
	
	// provjera unešenog broja - da li je u traženom intervalu
	if(br_filozofa < BRFILOZOFA_MIN){
		printf("Broj filozofa nije dovoljan!\n");
		printf("Unesite broj filozofa između 3 i 10.\n");
		return 0;
	}

	if(br_filozofa > BRFILOZOFA_MAX){
		printf("Broj filozofa je prevelik! Nema dovoljno hrane!\n");
		printf("Unesite broj filozofa između 3 i 10.\n");
		return 0;
	}

	// inicijaliziraj cjevovode
	for (int i = 0; i < br_filozofa; i++) {
        	for (int j = 0; j < br_filozofa; j++) {
            		if(i != j) {
				pipe(cj[i][j]);
            		}
        	}
	}

	int p;
	p = rand() % 10;

	// stvori procese (filozofe)
	for (int i = 0; i < br_filozofa; i++) {
		switch (fork()) {
			case -1:
				printf("Problem s kreiranjem filozofa\n");
				break;
			case 0:
				for(int j=0; j < i + 5; j++)
					sat = rand() % 10 + 1;	//nasumično postavljanje sata
				
				printf("Dolazak filozofa %d na konferenciju.\n", i);
				sleep(3);
				filozof(i, sat);	// funkcija za inicijalizaciju procesa filozofa
				break;	
		}
		pospan(p);		//spavaj nasumičan broj milisekundi između 100 i 2000;
						// funkcija rand pozvana je prije for petlje da se osigura da svi filozofi jednako spavaju
						//u protivnom se može dogoditi da dva već počnu s konferencijom, a treći je tek došao

		if(getpid() != pid)	//izađi iz petlje ako si ostao u procesu filozofa (greška), a trebao si se vratiti u glavni proces
			break;
	}

	if(getpid() == pid) {		//ako je sve u redu (nalazimo se ponovno u procesu roditelju) pričekaj da svi završe i završi program
		printf("\n");
		sigset(SIGINT, retreat);
		j = 0;
		while (j < br_filozofa) {
        	wait(NULL);
            j++;
        }

        printf("Kraj programa\n");
	}
	
	exit(0); // zatvori deskriptore
}
