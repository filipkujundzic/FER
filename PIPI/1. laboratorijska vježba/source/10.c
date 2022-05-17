#include <stdio.h>

int main(void)
{
	int x;
	scanf("%d",&x);
	if(x == (x%10)*(x%10)*(x%10) + ((x/10)%10)*((x/10)%10)*((x/10)%10) + (x/100)*(x/100)*(x/100))
		printf("Broj %d je Armstrongov broj.",x);
	return 0;
}