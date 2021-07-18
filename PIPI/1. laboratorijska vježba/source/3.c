#include <stdio.h>

int main(void)
{
	int x,x1;
	scanf("%d",&x);
	if(x<0) x1=-x;
	else x1=x;
	printf("Srednja znamenka broja %d je %d",x,(x1/10)%10);
	return 0;
}
