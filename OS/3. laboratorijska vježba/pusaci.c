#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<pthread.h>
#include<unistd.h>

#define PUSACI 3
#define BR_SASTOJAKA 3

pthread_mutex_t monitor;
pthread_cond_t uvjet;

pthread_cond_t red_uvjeta[PUSACI+1];

int stol[BR_SASTOJAKA-1];

// papir = 0 ; duhan = 1; sibice = 2;

int stol_prazan = 0;

int pusac_nema(int sastojak){
	if(sastojak == 0) return 2;
	if(sastojak == 1) return 1;
	if(sastojak == 2) return 0;
	return -1;
}

char *pretvori(int sastojak){
	
	if(sastojak == 0) return "papir";
	if(sastojak == 1) return "duhan";
	if(sastojak == 2) return "sibice";
	return "";		
}

void *Trgovac(void *args){
	//printf("Stvoren je trgovac %d %d",stol[0],stol[1]);
	int sastojak1, sastojak2;
	char *s1, *s2;
	srand(getpid());	

	while(1){

		pthread_mutex_lock(&monitor);

		while(stol_prazan == 1)
                        pthread_cond_wait(&uvjet, &monitor);
		
		sastojak1 = rand()%3;
		do{
			sastojak2 = rand()%3;
		}while(sastojak1 == sastojak2);
		//printf("Rand zavrsio %d %d",sastojak1,sastojak2);
		s1 = pretvori(sastojak1);
                s2 = pretvori(sastojak2);
		
		printf("Trgovac stavlja: %s(%d) i %s(%d)\n", s1,sastojak1,s2,sastojak2);

		stol[0] = sastojak1;
		stol[1] = sastojak2;
			
		stol_prazan = 1;
		
		for(int i = 0; i < PUSACI; ++i)
			pthread_cond_broadcast(&red_uvjeta[i]);
		
		pthread_mutex_unlock(&monitor);
		sleep(1);
	}
}

void *Pusac(int *p){

	while(1){
		pthread_mutex_lock(&monitor);
		int imam_sastojak = *(int *)p;		
		//printf("Stol[0] %d\n",stol[0]);
		//printf("Stol[1] %d\n",stol[1]);
		
		while(stol[0]==imam_sastojak || stol[1]==imam_sastojak || stol[0]<0 || stol[1]<0)
			pthread_cond_wait(&red_uvjeta[imam_sastojak], &monitor);	
			
		printf("Pusac %d  uzima sastojke i...\n\n",imam_sastojak);
		stol_prazan = 0;

		pthread_cond_broadcast(&uvjet); 		
		pthread_mutex_unlock(&monitor);
		sleep(2);
	}
}	

int main(int argc, char *argv[]){

	stol[0] = -1;
	stol[1] = -2;		
	srand(time(NULL));
	
	int i;
	int polje[PUSACI];
	
	pthread_t trg;
	pthread_t thr_id[PUSACI+1];

	pthread_mutex_init(&monitor, NULL);
	pthread_cond_init(&uvjet, NULL);

	
	for(int i = 0; i < PUSACI; ++i)
		pthread_cond_init(&red_uvjeta[i],NULL);

	pthread_create(&trg, NULL, Trgovac, NULL);
	for(i = 0; i < PUSACI; ++i){
		polje[i] = i;
		pthread_create(&thr_id[i], NULL, Pusac, (void *)&polje[i]);
		char *a = pretvori(i);		
		printf("Pusac %d ima sastojak %s\n", i, a); 
	}
	
	for(i = 0; i < PUSACI; ++i)
		pthread_join(thr_id[i],NULL);

	pthread_join(trg,NULL);
	return 0;	
}


