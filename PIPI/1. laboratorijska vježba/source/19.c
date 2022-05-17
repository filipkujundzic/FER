#include <stdio.h>

int main(void)
{
	int x,y;
	scanf("%d %d",&x,&y);
	if(x==y) 
		{
			printf("Brojevi moraju biti razliciti");
			return;
		}
	else 
		{
			if(x%y==0) printf("Broj %d je visekratnik broja %d.",x,y);
			if(y%x==0) printf("Broj %d je visekratnik broja %d.",y,x);
			if(x%y!=0 && y%x!=0) printf("Niti jedan ucitani broj nije visekratnik drugog ucitanog broja.");
		}
	return 0;
}