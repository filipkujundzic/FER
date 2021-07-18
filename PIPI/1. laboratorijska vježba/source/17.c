#include <stdio.h>

int main(void)
{
	float x;
	int p;
	scanf("%f %d",&x,&p);
	if(x<0) 
		{
			printf("Cijena mora biti pozitivni broj.");
			return;
		}
	if(p<0) 
		{
			printf("Postotak snizenja mora biti prirodni broj.");
			return;
		}
	printf("Cijena %.2f umanjena za %d posto iznosi %.2f.",x,p,x-(1.0*p/100)*x);
	return 0;
}