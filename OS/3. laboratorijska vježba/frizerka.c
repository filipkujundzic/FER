#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<semaphore.h>
#include<unistd.h>

#define CEKAONICA_MAX 10

sem_t OTVOREN; // postavlja se kada je salon otvoren
sem_t CEKAONICA; // ogranicava broj klijenata koji mogu cekati u jednom t
sem_t SPAVAJ; // frizerka spava
sem_t SISANJE; // klijent ceka da mu frizura bude gotova

int svi_gotovi = 0;
int cekaonica = 0; //broj ljudi u cekaonici
int otvoren = 0;

void *frizerka(void *args){

	printf("Frizerka: Evo sada cu otvoriti, znam da kasnim!\n");
	sem_post(&OTVOREN);
	otvoren = 1;
	printf("Frizerka: Salon je otvoren.\n");

	while(!svi_gotovi){
	
		printf("Frizerka: spavam dok klijenti ne dodu.\n"); 
		sleep(2);
		sem_wait(&SPAVAJ); // cekaj da me netko probudi 
		if(cekaonica) printf("Frizerka: idem raditi\n");
		sem_post(&CEKAONICA);
		if(!svi_gotovi){
			sleep(3);
			sem_post(&SISANJE);
			printf("Frizerka: klijent gotov\n");
		}
		else{
			printf("Radno vrijeme je zavrsilo!\n");
			otvoren = 0;
		}
	}
	
}		


void *klijent(void *broj){
	int br = *(int *)broj;
	if(otvoren){
		printf("Klijent (%d): Zelim na frizuru\n", br);
		if(cekaonica < CEKAONICA_MAX){
			printf("Klijent (%d): ulazim u cekaonicu!\n", br);
			cekaonica++;
			sem_post(&SPAVAJ);
			sem_wait(&CEKAONICA);
			cekaonica--;
			printf("Klijent (%d): Frizerka mi radi frizuru\n",br);
			sem_wait(&SISANJE);
		}
		else printf("Klijent (%d): Nema mjesta u cekaonici\n",br);
	}else printf("Nista od frizure danas, zatvoreno!");
}

void inicijaliziraj_semafore(){
	sem_init(&OTVOREN,0,0);
	sem_init(&CEKAONICA, 0,0);
	sem_init(&SPAVAJ,0,0);
	sem_init(&SISANJE,0,0);
}

int main(int *argc, char *argv[]){

	int klijenti =15;
	int i;
	int polje[klijenti];	
	
	pthread_t frizer;
	pthread_t thr_id[klijenti];
	pthread_t dodatni;	

	inicijaliziraj_semafore();
	
	for(i = 0; i < klijenti; i++){
		polje[i] = i;
	}

	//stvori dretvu frizerka
	pthread_create(&frizer, NULL, frizerka, NULL);

	sem_wait(&OTVOREN);	
	//stvori klijente
	for(i = 0; i < klijenti; i++){
		pthread_create(&thr_id[i],NULL,klijent,(void *)&polje[i]);
	}
	
	for(i = 0; i < klijenti; i++){
		pthread_join(thr_id[i], NULL);
	}	
	
	svi_gotovi = 1;
	sem_post(&SPAVAJ);
	pthread_join(frizer, NULL);
	
//	printf("Naknadno stvoreni klijent\n");
//	pthread_create(&dodatni, NULL, klijent, 42);	
//	pthread_join(&dodatni, NULL);
	
	return 0;
}
