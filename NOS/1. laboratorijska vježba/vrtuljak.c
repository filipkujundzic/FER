/*
Napredni operacijski sustavi
1. laboratorijska vježba
zadatak 1a
Vrtuljak.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <signal.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

typedef struct my_msgbuf {
    long mtype;
    char mtext[200];
}buf;

int msqid;

void retreat(int failure) 
{
    if (msgctl(msqid, IPC_RMID, NULL) == -1) {
        perror("msgctl");
        exit(1);
    }
    exit(0);
}

int sjedni_n = 0; // Broj poslanih dopuštenja posjetiteljima da sjednu na vrtuljak
int request_n = 0; // Broj zahtjeva primljenih od posjetitelja

// Funkcija kojom vrtuljak prima zahtjev posjetitelja za vožnjom
void recieve_request(int msqid){
	long mtype = 1;
	buf msg;
	if (msgrcv(msqid, (struct msgbuf *)&msg, sizeof(msg.mtext), mtype, 0) == -1) {
		perror("msgrcv");
		exit(1);
    }
	request_n += 1; // povećavamo brojač zahtjeva primljenih od posjetitelja
	//printf("[vrtuljak] Vrtuljak primio poruku: %s. Broj poruke: %d\n", msg.mtext,request_n);
	//Zbog urednijeg ispisa, printf poruke je izostavljen.
}

// Funkcija kojom vrtuljak šalje dopuštenje posjetitelju da sjedne
void send_sit(int msqid){
	long mtype = 2;
	sjedni_n += 1;		// povećavamo brojač poslanih dopuštenja
	buf msg = {mtype,"Sjedni"};
	if (msgsnd(msqid, (struct msgbuf *)&msg, strlen(msg.mtext)+1, 0) == -1){
			perror("msgsnd");
			exit(EXIT_FAILURE);
	}
	//printf("[vrtuljak] Vrtuljak šalje poruku: %s\n", msg.mtext);
}

// Funkcija kojom vrtuljak šalje poruku posjetitelju da ustane
void send_stand_up(int msqid){
	long mtype = 3;
	buf msg = {mtype,"Ustani"};
	if (msgsnd(msqid, (struct msgbuf *)&msg, strlen(msg.mtext)+1, 0) == -1){
			perror("msgsnd");
			exit(EXIT_FAILURE);
	}
	//printf("[vrtuljak] Vrtuljak šalje poruku: %s\n", msg.mtext);
	//Zbog urednijeg ispisa, printf poruke je izostavljen.
}


int main(){

	key_t key;
	key = getuid();
	
	buf *ptr = (buf*)malloc(sizeof(buf));
	
	// Kreiraj novi ili se spoji na postojeći message queue
	if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) { 
		perror("msgget");
        exit(1);
    }
	
	int spavaj;
	while(true) {
      	
        recieve_request(msqid);				// čekaj da posjetitelji zažele vožnju
		
		if(request_n <= 4)					// ako je broj zahtjeva manji od 4 (veličina vrtuljka)
			send_sit(msqid);				// pošalji poruku da posjetitelji mogu sjesti
		
		if(request_n == 4 && sjedni_n == 4){	// ako su primljena 4 zahtjeva za vožnjom i poslana 4 odobrenja
			sleep(1);							// pričekaj da svi posjetitelju uđu 
			printf("\nVrtuljak se pokreće\n");	// pokreni vrtuljak
			srand(time(NULL)); 					// osigurano pomoću pid da svaki put drugačije čeka 
			spavaj = (rand() % (3000 - 1000)) + 1000; // slučajno vrijeme spavanja
			sleep(spavaj/1000);					// vožnja u tijeku
			printf("\nZavršila vožnja\n");
			for(int i = 0; i < 4; i++)			//svakome od 4 posjetitelja pošalji poruku da ustanje
				send_stand_up(msqid);			
			sleep(1);							//pričekaj da svi ustanu
			request_n = 0;						// resetiraj brojače
			sjedni_n = 0;
		}		
	}
}

