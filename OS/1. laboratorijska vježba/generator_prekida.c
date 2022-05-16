#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

static int pid = 0;

void prekidna_rutina(int sig){
	kill(pid, SIGKILL);
	exit(0);
}

int main(int argc, char *argv[]){

	int i, j;
	pid = atoi(argv[1]);
	sigset(SIGINT, prekidna_rutina);
	srand((unsigned )time(NULL));

	while(1){
		i = rand() % 3 + 5;
		sleep(i);
		j = rand() % 4 + 1;
		switch(j) {
			case(1): kill(pid, SIGUSR1);
				break;
			case(2): kill(pid, SIGUSR2);
				break;
			case(3): kill(pid, SIGTERM);
				break;
			case(4): kill(pid, SIGQUIT);
				break;
		}
	}
	return 0;
}
