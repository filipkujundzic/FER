#include <stdio.h>

int main(void)
{
	int x,y;
	scanf("%d %d",&x,&y);
	if(x+y>0) printf("Aritmeticka sredina brojeva %d i %d: %.4f",x,y,(1.0*(x+y))/2);
	else 
		{
			if(1.0*((1./x)+(1./y))<0) printf("Izracunata vrijednost: %.4f",-1*(1.0*((1./x)+(1./y))));
			else printf("Izracunata vrijednost: %.4f",(1.0*((1./x)+(1./y))));
		}
	return 0;
}