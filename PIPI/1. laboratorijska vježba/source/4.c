#include <stdio.h>

int main(void)
{
	int x;
	scanf("%d",&x);
	if(x<0) printf("Neispravan broj");
	else 
	{
		if(x%2==0) printf("Broj %d je parni broj.",x);
		else printf("Broj %d je neparni broj.",x);
	}
	return 0;
}