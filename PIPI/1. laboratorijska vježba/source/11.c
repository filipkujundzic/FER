#include <stdio.h>

int main(void)
{
	int x;
	scanf("%d",&x);
	if(x%10 == x/100) printf("Broj %d je palindrom.",x);
	else printf("Broj %d nije palindrom.",x);
	return 0;
}