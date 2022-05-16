#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <pthread.h>

int n,m;

int *trazim,*broj;
int zadnji;
int ima;
int *stol;

void udi_u_kriticni_odsjecak(int i){
  int j;

  trazim[i] = 1;
  broj[i] = ++ zadnji;
  trazim[i] = 0;

  for(j = 1; j <= n; j++){
    while(trazim[j] != 0);
    while(broj[j] != 0 && (broj[j] < broj[i] || (broj[j] == broj[i] && j < i )));
  }
}

void izadi_iz_kriticnog_odsjecka(int i){
  broj[i] = 0;
}

void* obradi(void * p){
  srand(time(NULL));
  int j;
  int i = *((int*)p);
  int stol_index;
  while(ima){
    sleep(1);
    stol_index = rand()%m;
    printf("Dretva %d odabire stol %d\n",i,stol_index);
    udi_u_kriticni_odsjecak(i);

    if(stol[stol_index])
      printf("Neuspjela rezervacija %d. stola. Dretva: %d\n",stol_index,i);
    else{
      stol[stol_index] = i;
      printf("Rezerviran stol %d. Dretva %d\n",stol_index,i);
      ima--;
    }
    for(j = 0; j < m; j++){
      if(stol[j]){
        printf("%d ",stol[j]);
      }
      else
        printf("- ");
    }
    printf("\n");

    izadi_iz_kriticnog_odsjecka(i);
  }
}

int main(int argc, char *argv[]){

  int i;

  n = atoi(argv[1]);
  m = atoi(argv[2]);
  pthread_t polje[n + 1];
  pthread_t pom[n + 1];	
  ima = m;

  trazim = (int *)malloc((n + 1) * sizeof(int));
  broj = (int *)malloc((n + 1) * sizeof(int));
  stol = (int *)malloc(m * sizeof(int));

  memset(trazim,0,sizeof(trazim));
  memset(broj,0,sizeof(broj));
  memset(stol,0,sizeof(stol));

  for(i = 1; i <= n; i++){
    pom[i] = i;
    if(pthread_create(&polje[i],NULL,obradi,&pom[i]) !=0){
      printf("Creating thread #%d. was unsuccessful!!!\n",i);
    }
  }

  for(i = 1; i <= n; i++){
    pthread_join(polje[i],NULL);
  }

  free(trazim);
  free(broj);
  free(stol);

  return 0;
}
