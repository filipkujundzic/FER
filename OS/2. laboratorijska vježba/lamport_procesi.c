#include<stdio.h>
#include<stdlib.h>
#include<signal.h>
#include<sys/types.h>
#include<sys/ipc.h>
#include<sys/shm.h>

int segment_id;
int *trazim;
int *broj;
int *stol;

int rand_generator(int min, int max){
	int r = rand() % (max + 1 -min) + min;
	return r;
}

int nadi_najveci(int *broj, int n){
	int i;
	int  max = broj[0];
	for(i = 0; i < n; i++){
		if(broj[i] > max){
			max = broj[i];
		}
	}
	return max;
} 

void udi_u_ko(int i, int *trazim, int *broj, int velicina){
	trazim[i] = 1;
	broj[i] = nadi_najveci(broj, velicina) + 1;
	trazim[i] = 0;
	int j;
	int ulazni;
	int posluzeni;
	for(j = 0; j < velicina; j++){
		ulazni = trazim[j];
		while(ulazni == 1){
			ulazni = trazim[j];
		}
 		posluzeni = broj[i];
		while((posluzeni != 0) && (posluzeni < broj[i] || (posluzeni == broj[i] && j < i))){
		posluzeni = broj[j];
		}
	}
}

void izadi_iz_ko(int *broj, int id){
	broj[id] = 0;
}

void ispis_stolova(int *polje_stolova, int velicina){
	int c;
	int a;
	for(c = 0; c < velicina; c++){
		a = *(polje_stolova + c);
		if(a == '-'){
			printf("%2c ", a);
		}
		else{
			printf("%2d ", a);
		}
	}
	printf("\n");
}

void isprazni_stolove(int *polje_stolova, int velicina){
	int c;
	for(c = 0; c < velicina; c++){
		polje_stolova[c] = '-';
	}
	printf("\n");
}

void obradi(int id, int m, int n){
	printf("PID: %d\n",getpid());

	int c;
	int slobodan = 1;
	int broj_stola;
	int rezerviran = 0;
	while(slobodan == 1){
		sleep(1);
		for(c = 0; c < m; c++){
			slobodan = 0;
			if(*(stol + c) == '-'){
				slobodan = 1;
				break;
			}
		}
		if(slobodan == 0){
			continue;
		}
		
		broj_stola = rand_generator(0, m -1);
		udi_u_ko(id, trazim, broj, n);
		if(stol[broj_stola] == '-'){
			stol[broj_stola] = id;
			rezerviran = 1;
			printf("Process  %d: stol %d je rezerviran, stanje: ", id, broj_stola + 1);
		}
		else{
			printf("Process %d: stol %d nije rezerviran, stanje: ", id, broj_stola + 1);
		}
		izadi_iz_ko(broj, id);
		ispis_stolova(stol, m);
	}
}

void obrisi(int sig){
	(void)shmdt((char *)trazim);
	(void)shmdt((char *)stol);
	(void)shmdt((char *)broj);
	(void)shmctl(segment_id, IPC_RMID, NULL);
	exit(0);
}

int main(int argc, char *argv[]){
	srand((unsigned)time(NULL));
	int segment_velicina;
	int n = atoi(argv[1]);
	int m = atoi(argv[2]);

	sigset(SIGINT, obrisi);
	
	int dijeljena_segment_velicina = sizeof(int) * n * n;
	
	segment_id = shmget(IPC_PRIVATE,dijeljena_segment_velicina,0600);
	if(segment_id == -1){
		printf("Nema memorije!");
		exit(1);
	}
	
	trazim = (int *)shmat(segment_id, 0, 0);
	broj = (int *)shmat(segment_id, NULL,0) + (n +1) * sizeof(int);
	stol = (int *)shmat(segment_id,NULL,0) + 2*(n +1)* sizeof(int);

	printf("Imamo %d procesa i %d stolova\n", n,m);
	isprazni_stolove(stol,m);	
	int i;
	for(i = 0; i < n; i++){
		printf("Id napravljenog procesa je: %d", i + 1);
		switch(fork()){
		case 0:
			obradi(i +1, m, n);
			exit(0);
		case -1:
			printf("Nemoguće napraviti proces: %d", i +1);
		default:
			printf("Main radi nešto drugo...\n");
			continue;
		}
	}
	while(i--){
		(void)wait(NULL);
	}
	printf("Desk status is: ");
	ispis_stolova(stol, m);

	obrisi(0);
	return 0;
}
