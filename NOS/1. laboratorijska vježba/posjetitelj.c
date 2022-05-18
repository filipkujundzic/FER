/*
Napredni operacijski sustavi
1. laboratorijska vježba
zadatak 1a
Posjetitelj.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <time.h>
  
typedef struct my_msgbuf {
    long mtype;
    char mtext[200];
}buf;

// Funkcija kojom posjetitelj šalje poruku "Želim se voziti"
void request_ride(int msqid){
	long mtype = 1;			// tip poruke osigurava da ju ne pročita onaj read kojem nije namijenjena

	buf msg = {mtype, "Želim se voziti"};
	if (msgsnd(msqid, (struct msgbuf *)&msg, strlen(msg.mtext)+1, 0) == -1){
			perror("msgsnd");
			exit(EXIT_FAILURE);
	}
	//Zbog urednijeg ispisa, printf poruke je izostavljen.
}

// Funkcija kojom posjetitelj prima poruku da može sjesti i ispisuje da je sjeo
void recieve_sit(int msqid, int process_id){
	long mtype = 2;
	buf msg;
	if (msgrcv(msqid, (struct msgbuf *)&msg, sizeof(msg.mtext), mtype, 0) == -1) {
		perror("msgrcv");
		exit(1);
    }
	printf("Posjetitelj %d je sjeo.\n", process_id);
}


// Funkcija kojom posjetitelj prima poruku da je vožnja završila i da može ustati. Ispisuje da je ustao uz svoj id.
void stand_up(int msqid, int process_id){
	long mtype = 3;
	buf msg;
	if (msgrcv(msqid, (struct msgbuf *)&msg, sizeof(msg.mtext), mtype, 0) == -1) {
		perror("msgrcv");
		exit(1);
    }
	printf("Posjetitelj %d je ustao.\n", process_id);
}

int main(void) 
{ 
	int msqid;
	key_t key;
	key = getuid();
	
	// Kreiraj novi ili se spoji na postojeći message queue
	if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) {
        perror("msgget");
        exit(1);
    }

	int spavaj;
	printf("[posjetitelj] Ja sam posjetitelj %d\n", getpid()); // posjetitelji se razlikuju po pid-u
	buf *ptr = (buf*)malloc(sizeof(buf));

	for(int i = 0; i < 3; i++){
		srand(time(NULL) + getpid() + i); 			// osigurano pomoću pid da svaki put drugačije čeka
		spavaj = (rand() % (2000 - 100)) + 100; 		// slučajno vrijeme spavanja
		sleep(spavaj/1000); 					// pretvaranje u milisekunde - spavaj x milisekundi

		request_ride(msqid); 						// pošalji poruku "Želim se voziti"

		recieve_sit(msqid, getpid());				// primi poruku da možeš sjesti

		stand_up(msqid, getpid());					// primi poruku da možeš ustati
						
	}
	printf("Posjetitelj %d je gotov!\n", getpid()); // posjetitelj javlja da je gotov - bez obzira ako je to u 
							// trenutku ulaska/silaska na vrtuljak drugih posjetitelja
							// navedeno je dopušteno jer više nije u kritičnom odsječku
	
	return 0;
	     
}
