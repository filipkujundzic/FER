#include <stdio.h>

int main(void)
{
	int x;
	scanf("%d",&x);
	printf("Umnozak znamenaka broja %d je %d",x,(x%10)*((x/10)%10)*(x/100));
	return 0;
}