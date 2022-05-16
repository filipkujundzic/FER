#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <math.h>

#define INTERVAL 5
#define _XOPEN_SOURCE 
#define _XOPEN_SOURCE_EXTENDED


int  broj =  1000000001;
int  zadnji =  1000000001;
int pauza = 0;

void periodicki_ispis(int signal){
	printf( "Zadnji prosti broj = %d\n" , zadnji);
}

int postavi_pauzu(int signal){
	pauza = 1 - pauza;
	return pauza;
}

void prekini(int signal){
	printf( "%d" , zadnji);
	exit(0);
}

int prost(unsigned long n){
	
	unsigned long i, max;
	if( ( n&1 ) == 0)
		return 0;
	
	max = sqrt(n); 
	for( i = 3; i <= max; i += 2)
		if((n % i) == 0)
			return 0;

	return 1;
}

void postavi_periodicki_alarm(struct itimerval t, int sekunde){
	t.it_value.tv_sec = sekunde;
	t.it_value.tv_usec = sekunde * 100000;
	t.it_interval.tv_sec = sekunde;
	t.it_interval.tv_usec = sekunde * 100000;

	setitimer (ITIMER_REAL, &t, NULL);
}

int main(void){

	unsigned long i;

	sigset (SIGTERM, prekini ); 
	sigset (SIGALRM, periodicki_ispis);
	sigset (SIGINT, postavi_pauzu);

	struct itimerval t;
	postavi_periodicki_alarm(t, INTERVAL);
	while(1){
		if (prost(broj) == 1)
			zadnji = broj;
		broj++;
		while (pauza == 1)
			pause();
	}
	return 0;
}

