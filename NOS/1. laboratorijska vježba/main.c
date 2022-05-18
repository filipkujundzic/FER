/*
Napredni operacijski sustavi
1. laboratorijska vježba
zadatak 1a
Main.c
*/

#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

int msqid;

void retreat(int failure) 
{
    if (msgctl(msqid, IPC_RMID, NULL) == -1) {
        perror("msgctl");
        exit(1);
    }
    exit(0);
}

int main(int argc, char *argv[]){
	
	key_t key;
	key = getuid();		// za ključ koristimo user id
	
	if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) {
        	perror("msgget");
        	exit(1);
    	}

	sigset(SIGINT, retreat);

    	// dolazak posjetitelja
	for(int i = 0; i < 8; i++){
		switch (fork()) {
			case -1:
				printf("Nema posjetitelja.\n");
				break;
			case 0:
				execl("./posjetitelj","posjetitelj",NULL);
				exit(EXIT_SUCCESS);
		}
	}	
	
	sleep(1);	// čekanje svih posjetitelja
	
	// pokretanje vrtuljka
	switch (fork()) {
		case -1:
			printf("Nije moguće pokrenuti vrtuljak.\n");
			break;
		case 0:
			execl("./vrtuljak","vrtuljak",NULL);
			exit(EXIT_SUCCESS);
		default: 
			sleep(1);
	}
	while(1);

}
