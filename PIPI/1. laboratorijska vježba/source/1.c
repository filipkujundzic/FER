#include <stdio.h>

int main(void)
{
	int x;
	scanf("%d",&x);
	if(x%10 < 5) printf("Zadnja znamenka broja %d je %d",x,x%10);
	else printf("Zadnje dvije znamenke broja %d su %d",x,x%100);
	return 0;
}