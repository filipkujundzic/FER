#include <stdio.h>

int main(void)
{
	int x,x1=0;
	scanf("%d",&x);
	x1=x%10*100+((x/10)%10)*10+x/100;
	printf("Broj dobiven obrnutim poretkom znamenaka broja %d je %d.",x,x1);
	return 0;
}
	