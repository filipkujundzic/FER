#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int A;

void *Povecaj(void *x){
	int b = *((int*)x);
	A += b;
}

int main(int argc, char *argv[]){
		
	int N,M,i;

	A = 0;
	N = atoi(argv[1]);
	M = atoi(argv[2]);
	pthread_t thr_id[N];
	
	for(i = 0; i < N; i++){	
		pthread_create(&thr_id[i], NULL, Povecaj, &M);
		pthread_join(thr_id[i],NULL);
	}
				
	printf("A = %d\n", A);	
	
	return 0;

}

